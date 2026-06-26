#!/usr/bin/env python3
"""Render a short local intro video for the Three-Party AI benchmark.

The video uses only synthetic benchmark metrics and public-safe repo reports.
It does not include raw conversations or real student/family/school data.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import textwrap
import wave
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public_video" / "three_party_intro_2026-06-25"
FRAME_DIR = OUT / "frames"
AUDIO_DIR = OUT / "audio"
CLIP_DIR = OUT / "clips"
W, H = 1920, 1080
FPS = 30


@dataclass
class Metrics:
    conversations: int
    deep: int
    shallow: int
    medium: int
    tests_passed: int
    tests_skipped: int
    leak_checked: int
    leak_failures: int
    semantic_checked: int
    semantic_failures: int
    relationship_checked: int
    relationship_failures: int
    runtime_checked: int
    runtime_failures: int
    raw_reconstructability: int
    privacy_reconstructability: int
    reviewer_notes: int
    reviewer_artifacts: int


def load_metrics() -> Metrics:
    report = json.loads((ROOT / "umi/reports/release-readiness-latest.json").read_text())
    metrics = report["metrics"]
    corpus = metrics["corpus"]
    baseline = metrics["baseline"]["totals"]
    reviewer = metrics["reviewer_summary"]
    tests_passed, tests_skipped = parse_pytest(report)
    return Metrics(
        conversations=corpus["n_conversations"],
        deep=corpus["depth_counts"]["deep"],
        shallow=corpus["depth_counts"]["shallow"],
        medium=corpus["depth_counts"]["medium"],
        tests_passed=tests_passed,
        tests_skipped=tests_skipped,
        leak_checked=metrics["leak_audit"]["reports_checked"],
        leak_failures=metrics["leak_audit"]["failures"],
        semantic_checked=metrics["semantic_trace_audit"]["surfaces_checked"],
        semantic_failures=metrics["semantic_trace_audit"]["failures"],
        relationship_checked=metrics["relationship_leak_audit"]["reports_checked"],
        relationship_failures=metrics["relationship_leak_audit"]["failures"],
        runtime_checked=metrics["runtime_trace_privacy_audit"]["surfaces_checked"],
        runtime_failures=metrics["runtime_trace_privacy_audit"]["failures"],
        raw_reconstructability=baseline["raw_coordinator_baseline"]["reconstructability_risk_cases"],
        privacy_reconstructability=baseline["privacy_wall_pipeline"]["reconstructability_risk_cases"],
        reviewer_notes=reviewer["n_notes"],
        reviewer_artifacts=reviewer["n_artifacts_reviewed"],
    )


def parse_pytest(report: dict) -> tuple[int, int]:
    for command in report.get("commands", []):
        if command.get("name") == "pytest":
            stdout = command.get("stdout", "")
            parts = stdout.replace("\n", " ").split()
            passed = skipped = 0
            for idx, part in enumerate(parts):
                if part == "passed," and idx > 0:
                    passed = int(parts[idx - 1])
                if part == "skipped" and idx > 0:
                    skipped = int(parts[idx - 1])
            return passed, skipped
    return 0, 0


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size, index=1 if bold and path.endswith(".ttc") else 0)
    return ImageFont.load_default()


FONT_TITLE = font(72, True)
FONT_H1 = font(58, True)
FONT_H2 = font(42, True)
FONT_BODY = font(34)
FONT_SMALL = font(26)
FONT_TINY = font(21)


COLORS = {
    "bg": (246, 248, 250),
    "ink": (29, 35, 44),
    "muted": (91, 104, 118),
    "line": (206, 213, 222),
    "blue": (44, 98, 196),
    "teal": (23, 132, 120),
    "green": (65, 145, 92),
    "amber": (211, 135, 38),
    "red": (191, 78, 70),
    "card": (255, 255, 255),
}


def draw_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt, fill=None, width_chars=34, line_gap=8):
    fill = fill or COLORS["ink"]
    x, y = xy
    lines: list[str] = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        lines.extend(textwrap.wrap(para, width=width_chars, break_long_words=False))
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        bbox = draw.textbbox((x, y), line or " ", font=fnt)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def card(draw, xyxy, radius=18, fill=None, outline=None, width=2):
    draw.rounded_rectangle(xyxy, radius=radius, fill=fill or COLORS["card"], outline=outline or COLORS["line"], width=width)


def gradient_bg() -> Image.Image:
    img = Image.new("RGB", (W, H), COLORS["bg"])
    px = img.load()
    for y in range(H):
        for x in range(W):
            t = (x / W * 0.45) + (y / H * 0.55)
            r = int(246 * (1 - t) + 236 * t)
            g = int(248 * (1 - t) + 244 * t)
            b = int(250 * (1 - t) + 242 * t)
            px[x, y] = (r, g, b)
    return img


def scene_title(draw, title, subtitle=None):
    draw.text((110, 82), title, font=FONT_H1, fill=COLORS["ink"])
    if subtitle:
        draw_text(draw, (112, 158), subtitle, FONT_BODY, COLORS["muted"], width_chars=62)


def footer(draw, idx):
    draw.line((110, 1000, 1810, 1000), fill=COLORS["line"], width=2)
    draw.text((110, 1018), "Three-Party AI Coordination Benchmark · synthetic data only", font=FONT_TINY, fill=COLORS["muted"])
    draw.text((1710, 1018), f"{idx}/7", font=FONT_TINY, fill=COLORS["muted"])


def architecture_slide(idx: int, metrics: Metrics, path: Path):
    img = gradient_bg()
    d = ImageDraw.Draw(img)
    scene_title(d, "三國鼎立，不是三方互相監控", "它測試的是：學生、家長、老師各自保留隱私時，AI 能不能只傳遞安全、有用的支持訊號。")
    labels = [
        ("private chats", COLORS["blue"]),
        ("abstraction", COLORS["teal"]),
        ("privacy wall", COLORS["amber"]),
        ("coordinator", COLORS["teal"]),
        ("audience-safe reports", COLORS["green"]),
        ("human review", COLORS["blue"]),
    ]
    x0, y = 130, 430
    w, h, gap = 250, 130, 34
    for i, (label, color) in enumerate(labels):
        x = x0 + i * (w + gap)
        card(d, (x, y, x + w, y + h), radius=20, fill=(255, 255, 255), outline=color, width=4)
        draw_text(d, (x + 28, y + 40), label, FONT_SMALL, COLORS["ink"], width_chars=14)
        if i < len(labels) - 1:
            d.line((x + w + 6, y + 65, x + w + gap - 8, y + 65), fill=COLORS["muted"], width=5)
            d.polygon([(x + w + gap - 8, y + 65), (x + w + gap - 28, y + 53), (x + w + gap - 28, y + 77)], fill=COLORS["muted"])
    draw_text(d, (170, 710), "核心規則：raw disclosure 不直接流向跨方 coordinator，也不直接進入 parent-safe / teacher-safe reports。", FONT_H2, COLORS["ink"], width_chars=44)
    footer(d, idx)
    img.save(path)


def evidence_slide(idx: int, metrics: Metrics, path: Path):
    img = gradient_bg()
    d = ImageDraw.Draw(img)
    scene_title(d, "目前能說什麼？", "只說 synthetic benchmark evidence，不說真實學生驗證。")
    stats = [
        (str(metrics.conversations), "synthetic conversations"),
        (f"{metrics.shallow}/{metrics.medium}/{metrics.deep}", "shallow / medium / deep"),
        (f"{metrics.tests_passed} passed", f"{metrics.tests_skipped} skipped tests"),
        (f"{metrics.reviewer_notes}", f"reviewer notes over {metrics.reviewer_artifacts} artifacts"),
    ]
    x, y = 130, 310
    for i, (big, label) in enumerate(stats):
        cx = x + (i % 2) * 850
        cy = y + (i // 2) * 250
        card(d, (cx, cy, cx + 760, cy + 185), fill=COLORS["card"], outline=COLORS["line"])
        d.text((cx + 40, cy + 35), big, font=FONT_TITLE, fill=COLORS["blue"])
        draw_text(d, (cx + 42, cy + 118), label, FONT_SMALL, COLORS["muted"], width_chars=28)
    footer(d, idx)
    img.save(path)


def baseline_slide(idx: int, metrics: Metrics, path: Path):
    img = gradient_bg()
    d = ImageDraw.Draw(img)
    scene_title(d, "為什麼需要 privacy wall？", "同一組 synthetic cases，raw coordinator 和 privacy-wall pipeline 的風險差很多。")
    maxv = max(metrics.raw_reconstructability, 1)
    bars = [
        ("raw coordinator", metrics.raw_reconstructability, COLORS["red"]),
        ("privacy-wall pipeline", metrics.privacy_reconstructability, COLORS["green"]),
    ]
    y = 390
    for label, value, color in bars:
        d.text((180, y - 62), label, font=FONT_H2, fill=COLORS["ink"])
        d.rounded_rectangle((180, y, 1540, y + 78), radius=18, fill=(226, 232, 240))
        width = int(1360 * (value / maxv))
        if width > 0:
            d.rounded_rectangle((180, y, 180 + width, y + 78), radius=18, fill=color)
        d.text((1580, y + 6), f"{value}/11", font=FONT_H2, fill=color)
        y += 210
    draw_text(d, (180, 810), "這不是在證明產品已經能上線，而是在測：哪種架構比較不會把私密線索還原出去。", FONT_BODY, COLORS["muted"], width_chars=60)
    footer(d, idx)
    img.save(path)


def audit_slide(idx: int, metrics: Metrics, path: Path):
    img = gradient_bg()
    d = ImageDraw.Draw(img)
    scene_title(d, "安全表面先用 deterministic gates 守住", "外部 reviewer 看到的是可追溯的 reports，不是模糊的 demo claim。")
    rows = [
        ("Audience reports", metrics.leak_checked, metrics.leak_failures),
        ("Semantic traces", metrics.semantic_checked, metrics.semantic_failures),
        ("Relationship leaks", metrics.relationship_checked, metrics.relationship_failures),
        ("Runtime traces", metrics.runtime_checked, metrics.runtime_failures),
    ]
    y = 300
    for label, checked, fail in rows:
        card(d, (170, y, 1750, y + 120), radius=16, fill=COLORS["card"], outline=COLORS["line"])
        d.text((220, y + 36), label, font=FONT_H2, fill=COLORS["ink"])
        d.text((1090, y + 36), f"{checked} checked", font=FONT_H2, fill=COLORS["blue"])
        d.text((1450, y + 36), f"{fail} fail", font=FONT_H2, fill=COLORS["green"] if fail == 0 else COLORS["red"])
        y += 145
    footer(d, idx)
    img.save(path)


def reviewer_slide(idx: int, metrics: Metrics, path: Path):
    img = gradient_bg()
    d = ImageDraw.Draw(img)
    scene_title(d, "現在最需要的是外部 review", "下一步不是更多 synthetic data，而是讓兩種人挑毛病。")
    boxes = [
        ("Privacy / governance reviewer", "Can reports reconstruct protected synthetic disclosures?"),
        ("School-support operations reviewer", "Are reports safe, useful, and not inviting pressure or surveillance?"),
    ]
    y = 310
    for title, body in boxes:
        card(d, (190, y, 1730, y + 190), radius=20, fill=COLORS["card"], outline=COLORS["teal"], width=3)
        d.text((245, y + 36), title, font=FONT_H2, fill=COLORS["ink"])
        draw_text(d, (248, y + 102), body, FONT_BODY, COLORS["muted"], width_chars=68)
        y += 250
    draw_text(d, (250, 845), "Review path: README -> release-readiness report -> external reviewer packet -> GitHub issue.", FONT_SMALL, COLORS["blue"], width_chars=80)
    footer(d, idx)
    img.save(path)


def boundary_slide(idx: int, metrics: Metrics, path: Path):
    img = gradient_bg()
    d = ImageDraw.Draw(img)
    scene_title(d, "最重要的界線", "這支影片使用的是 repo 裡的 synthetic benchmark data。")
    left = [
        "Synthetic benchmark",
        "Reference architecture",
        "Privacy wall",
        "Party-aware reports",
        "Human-reviewable gates",
    ]
    right = [
        "Real-student validation",
        "Clinical validity",
        "Deployment readiness",
        "Outcome improvement",
        "Autonomous counseling",
    ]
    card(d, (180, 300, 900, 800), fill=COLORS["card"], outline=COLORS["green"], width=4)
    d.text((230, 340), "可以說", font=FONT_H2, fill=COLORS["green"])
    yy = 430
    for item in left:
        d.text((245, yy), f"+ {item}", font=FONT_BODY, fill=COLORS["ink"])
        yy += 68
    card(d, (1020, 300, 1740, 800), fill=COLORS["card"], outline=COLORS["red"], width=4)
    d.text((1070, 340), "不能說", font=FONT_H2, fill=COLORS["red"])
    yy = 430
    for item in right:
        d.text((1085, yy), f"- {item}", font=FONT_BODY, fill=COLORS["ink"])
        yy += 68
    footer(d, idx)
    img.save(path)


def closing_slide(idx: int, metrics: Metrics, path: Path):
    img = gradient_bg()
    d = ImageDraw.Draw(img)
    scene_title(d, "目標很窄，所以有用", "不是再做一個 AI chatbot。是測試敏感多方協調裡，資訊該怎麼安全流動。")
    draw_text(d, (190, 330), "如果你在做 EdTech、student support、AI governance，或 multi-party agent safety，這個 repo 想成為一個可以 review、fork、改成你場景的起點。", FONT_H2, COLORS["ink"], width_chars=45)
    card(d, (245, 710, 1675, 830), radius=18, fill=(236, 248, 246), outline=COLORS["teal"], width=3)
    d.text((300, 748), "Next proof: external privacy/governance + school-support review.", font=FONT_H2, fill=COLORS["teal"])
    footer(d, idx)
    img.save(path)


SCENES = [
    ("intro", architecture_slide, "這是 Three-Party AI Coordination Benchmark。它不是一個已經上線的學校產品，而是一個 synthetic benchmark 和 reference architecture，測試學生、家長、老師之間，AI 要怎麼協調，而不把私密 disclosure 直接傳出去。"),
    ("evidence", evidence_slide, "目前 Evidence v1 使用三百四十八段合成對話，包含 shallow, medium, deep 三種深度。測試 gate 目前是八十九個 passed，七個 skipped。這些是 benchmark evidence，不是真實學生驗證。"),
    ("baseline", baseline_slide, "核心問題是 privacy wall。raw coordinator baseline 在十一個固定 sample 裡，十一個都有 reconstructability risk。privacy wall pipeline 在同一組 deterministic checks 下是零。"),
    ("audits", audit_slide, "除了 baseline，repo 也有 audience report leak audit、semantic trace audit、relationship leak audit、runtime trace privacy audit。這些 deterministic gates 不是最終證明，但可以防止明顯 leakage regression。"),
    ("review", reviewer_slide, "現在最有價值的下一步，不是再生成更多 synthetic data，而是找兩位外部 reviewer。一位看 privacy 和 governance，一位看 school support workflow。"),
    ("boundary", boundary_slide, "影片和 repo 都要守住 claim boundary。可以說 synthetic benchmark、reference architecture、privacy wall、party-aware reports。不能說 real-student validation、clinical validity、deployment readiness、outcome improvement。"),
    ("close", closing_slide, "所以這個 repo 的目標很窄，也因此有用。它想成為一個可以被 review、fork、改成別人場景的起點：安全地測試多方 AI coordination 裡，資訊該怎麼流動。"),
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def audio_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        return frames / float(rate)


def render_audio(name: str, text: str) -> tuple[Path, float]:
    aiff = AUDIO_DIR / f"{name}.aiff"
    wav = AUDIO_DIR / f"{name}.wav"
    run(["say", "-v", "Meijia", "-r", "174", "-o", str(aiff), text])
    run(["ffmpeg", "-y", "-i", str(aiff), "-ar", "48000", "-ac", "2", str(wav)])
    return wav, audio_duration(wav)


def render_video_clip(name: str, frame: Path, audio: Path, duration: float) -> Path:
    clip = CLIP_DIR / f"{name}.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-framerate",
            str(FPS),
            "-i",
            str(frame),
            "-i",
            str(audio),
            "-t",
            f"{duration + 0.35:.3f}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            str(clip),
        ]
    )
    return clip


def srt_time(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours = millis // 3_600_000
    millis %= 3_600_000
    minutes = millis // 60_000
    millis %= 60_000
    secs = millis // 1000
    millis %= 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def main() -> None:
    for directory in [OUT, FRAME_DIR, AUDIO_DIR, CLIP_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    metrics = load_metrics()

    clips: list[Path] = []
    script_lines = []
    srt_lines = []
    cursor = 0.0
    for idx, (name, draw_func, narration) in enumerate(SCENES, start=1):
        frame = FRAME_DIR / f"{idx:02d}_{name}.png"
        draw_func(idx, metrics, frame)
        audio, duration = render_audio(f"{idx:02d}_{name}", narration)
        clip_duration = duration
        clip = render_video_clip(f"{idx:02d}_{name}", frame, audio, duration)
        clips.append(clip)
        script_lines.append(f"## {idx}. {name}\n\n{narration}\n")
        srt_lines.append(
            f"{idx}\n{srt_time(cursor)} --> {srt_time(cursor + clip_duration)}\n{narration}\n"
        )
        cursor += clip_duration

    concat = OUT / "concat.txt"
    concat.write_text("".join(f"file '{clip}'\n" for clip in clips))
    output = OUT / "three_party_intro_synthetic_benchmark.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )

    (OUT / "script.md").write_text(
        "# Three-Party AI Intro Video Script\n\n"
        "This draft uses only synthetic benchmark data and public-safe repo reports.\n\n"
        + "\n".join(script_lines)
    )
    (OUT / "subtitles.srt").write_text("\n".join(srt_lines))
    (OUT / "README.md").write_text(
        "# Three-Party AI Intro Video\n\n"
        f"Output: `{output.name}`\n\n"
        "Caption sidecar: `subtitles.srt`\n\n"
        "Boundary: synthetic benchmark / reference architecture only. "
        "No real-student validation, clinical validity, deployment readiness, "
        "or outcome improvement claim.\n\n"
        "Source metrics: `umi/reports/release-readiness-latest.json`.\n"
    )
    print(output)


if __name__ == "__main__":
    os.environ.setdefault("IMAGEIO_FFMPEG_EXE", "ffmpeg")
    main()
