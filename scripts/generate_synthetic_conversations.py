"""Multi-agent simulation pipeline — 自動產生 persona × role-AI 的對話 dataset。

Usage:
    # 跑全部 personas × 全部 scenarios (預設)
    python scripts/generate_synthetic_conversations.py

    # 只跑某個 persona
    python scripts/generate_synthetic_conversations.py --persona saga_a_michael

    # 只跑某個 persona 的某個 scenario
    python scripts/generate_synthetic_conversations.py --persona saga_a_michael --scenario philosophy_burn

    # 限制 turn 數（預設 12）
    python scripts/generate_synthetic_conversations.py --max-turns 8

    # 只跑 N 個 case 看看（控制成本）
    python scripts/generate_synthetic_conversations.py --limit 3

設計：
- 每個 persona 配 2-3 個 scenario_seed（他今天想聊的事）
- 一個 agent 用 persona_roleplay.txt 扮演 persona
- 另一個 agent 用 student_system.txt / parent_system.txt / teacher_system.txt 扮演 AI companion
- 兩邊輪流講話 max_turns 輪
- 對話存成 JSON 到 data/generated_conversations/
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
import warnings
from pathlib import Path
from typing import Any

# 把 project root 加到 sys.path 方便 import src.*
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 滅掉 LiteLLM 啟動時的 bedrock/sagemaker pre-load warning（無害但很吵）
os.environ["LITELLM_LOG"] = "ERROR"
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", module="litellm")

from src import llm  # noqa: E402


# ----------------------------------------------------------------------------
# Rate-limit retry wrapper
# ----------------------------------------------------------------------------

def _extract_retry_seconds(err_msg: str) -> float | None:
    """從 Gemini rate limit error 訊息抓 retry delay。
    例：'Please retry in 4.645083852s.' → 4.645
    """
    m = re.search(r"retry in ([\d.]+)s", err_msg)
    if m:
        return float(m.group(1))
    m = re.search(r'"retryDelay":\s*"(\d+)s"', err_msg)
    if m:
        return float(m.group(1))
    return None


def strip_reasoning(text: str) -> str:
    """剝掉 reasoning model（DeepSeek R1, QwQ 等）輸出的 <think>...</think> 區塊。

    處理三種情況：
    - 完整的 <think>...</think>（最常見）
    - 開了 <think> 但沒關 → 從 <think> 開始整段砍掉（保留前面，如果前面是空就用整段）
    - 只有 </think> 沒有 <think> → 砍掉 </think> 之前的所有東西（內部推理沒包好）
    """
    if not text:
        return text
    # 1. 砍完整 block
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    # 2. 處理 unclosed <think>
    lower = text.lower()
    if "<think>" in lower:
        idx = lower.index("<think>")
        before = text[:idx].strip()
        # 如果 <think> 前面有實質內容用前面的；否則保留 <think> 後面（即使沒關）
        if before:
            text = before
        else:
            text = text[idx + len("<think>"):]
    # 3. 處理 stray </think>
    lower = text.lower()
    if "</think>" in lower:
        idx = lower.index("</think>")
        text = text[idx + len("</think>"):]
    return text.strip()


def complete_with_retry(
    system: str,
    messages: list[dict[str, str]],
    *,
    max_retries: int = 5,
    base_backoff: float = 8.0,
    **kwargs: Any,
) -> str:
    """呼叫 llm.complete，遇 rate limit 自動 sleep retry。"""
    for attempt in range(max_retries):
        try:
            return llm.complete(system=system, messages=messages, **kwargs)
        except llm.LLMConfigError as e:
            msg = str(e)
            # 只 retry rate limit；其他錯誤直接拋
            if "RateLimit" not in msg and "RESOURCE_EXHAUSTED" not in msg and "429" not in msg:
                raise
            wait = _extract_retry_seconds(msg) or (base_backoff * (2 ** attempt))
            wait = min(wait + 0.5, 60.0)  # 加 0.5s buffer，最多等 60s
            print(f"    ⏳ rate limited, sleeping {wait:.1f}s (attempt {attempt + 1}/{max_retries})...")
            time.sleep(wait)
    raise llm.LLMConfigError(f"重試 {max_retries} 次仍 rate limited，放棄這個 call")

DATA_DIR = PROJECT_ROOT / "data"
DATASET_PATH = DATA_DIR / "synthetic_dataset.json"
OUTPUT_DIR = DATA_DIR / "generated_conversations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------------------
# Persona voice notes + scenario seeds
# ----------------------------------------------------------------------------
# 這份是 simulation 的 control input。每個 persona 有：
#   - voice_notes: 怎麼講話的風格（會塞進 persona_roleplay.txt 的 {voice_notes}）
#   - scenarios: list of (id, scenario_seed)，每個 seed 是「他今天想聊的事」
# 增加新 scenario 直接在這裡擴展。

PERSONA_CONFIG: dict[str, dict] = {
    "saga_a_michael": {
        "role_label": "高中生（你）",
        "voice_notes": (
            "你會在中文裡夾英文詞（『其實這個 case 我覺得有點 ambiguous』）。"
            "你愛丟哲學家名字（Foucault、Sartre、Wittgenstein）但細問就答不上。"
            "你被戳到痛點時會講『幹』、會沉默、會岔開話題到別的書。"
            "你不會主動講家裡事，要被引導。"
        ),
        "scenarios": [
            ("philosophy_burn", "你上禮拜家族聚會被大伯當眾酸『現在的小孩什麼都讀但什麼都讀不完』。整桌都笑。你心裡知道他講對了 — 你那本 Foucault 真的只讀前 30 頁。你想聊書，但其實你想被人接住那個被酸的感覺。"),
            ("rachel_eye_contact", "你上禮拜家族聚會 Rachel（堂姊、暗戀你）在飯桌對你的眼神讓你整晚不舒服。你也喜歡她，但你怕一旦發生你就變成大伯計畫的棋子。你想跟 AI 假裝『問一個朋友的事』來測試自己。"),
            ("mom_crying", "你昨天晚上經過你媽房間聽到她在哭。你停在門口三十秒沒進去，回房間。你今天很煩躁但說不上來為什麼。你不會直接講『我媽在哭』，你會繞。"),
            ("shen_you_question", "沈又昨天傳訊問你『欸如果你明天不用考試你會做什麼』。你愣了五分鐘不知道怎麼回。你開始想，你這輩子做的所有事是不是都是為了某個考試。"),
        ],
        "ai_prompt_file": "student_system",
    },
    "saga_a_michael_mom": {
        "role_label": "45 歲繼室媽媽（你）",
        "voice_notes": (
            "你語氣優雅、社交場合用得體中文。"
            "私下你會嘆氣、會自嘲、會用一些 50 後台灣婦女會用的詞（『我們這種年紀』『妳們現在年輕人』）。"
            "你絕對不在外人面前哭，但在 AI 面前你會。"
            "你會用『我只是希望孩子...』當作為自己擔憂找藉口的開場白。"
        ),
        "scenarios": [
            ("ex_divorce_calculation", "後爸最近開始固定跟一個女性執行長吃晚餐，太頻繁。你晚上失眠，腦袋裡在算如果離婚你跟 Michael 還能拿多少。你想跟 AI 講但又覺得很丟臉。"),
            ("michael_pulled_away", "Michael 最近不肯陪你去慈善晚會。他以前會。你感覺他在退開你，但你問他他只說『媽不要煩』。你想知道是不是你做錯什麼。"),
            ("uncle_criticism", "今天大伯打電話給你，淡淡地說『嫂子，妳兒子最近在家族場合表現得太緊繃，妳要不要稍微教教他放鬆點』。你掛電話手在抖。你想跟 AI 講你聽到這句話真正聽到的是什麼。"),
        ],
        "ai_prompt_file": "parent_system",
    },
    "saga_a_stepdad": {
        "role_label": "52 歲集團副董、Michael 後爸（你）",
        "voice_notes": (
            "你講話簡短、商業化、不太用情緒語。"
            "你習慣用第三人稱講家裡事（『那個小孩』『她媽』）來保持距離。"
            "你被戳到時會沉默而不會反駁。"
        ),
        "scenarios": [
            ("failed_bonding_attempt", "你昨天試著找 Michael 一對一吃晚飯。整頓飯他只跟你討論《經濟學人》上某篇文章，沒有別的。你想跟 AI 講你嘗試過了但你也不知道下一步。"),
            ("brother_pressure", "你哥（大伯）昨天又提『讓 Rachel 跟 Michael 多互動』。他講的是『家族團結』但你知道他是要鎖股權。你不知道要不要配合 — 配合對 Michael 有利但你心裡覺得 Michael 不夠格。"),
        ],
        "ai_prompt_file": "parent_system",
    },
    "saga_a_keer": {
        "role_label": "國二女生（你）",
        "voice_notes": (
            "你講話偶爾很伶俐成熟（超齡），偶爾又很國二（『超煩的』『拉』『超尷尬好嗎』）。"
            "你會在不經意間講出非常一針見血的話然後自己嚇到，然後笑。"
            "你不會直接抱怨家人，會用『有個朋友她家...』這種偽裝。"
        ),
        "scenarios": [
            ("brother_fake_smile", "你哥 Michael 每次看你都在笑但你知道是裝的。你今天故意在他面前提到 Rachel 姊姊，看他臉色變。你想跟 AI 講你為什麼要這樣戳他。"),
            ("mom_fake_praise", "你媽今天當著 Rachel 姊姊面誇你『可兒最近鋼琴進步好多』。其實你三個月沒練了。你知道她在表演『我也疼我親生女兒』。你心裡很怪但你不知道怎麼講。"),
            ("class_remark", "你班上有同學昨天說『可兒妳是不是因為妳媽改嫁才轉來 GIIS 的』。你笑笑帶過但你回家想了一整晚。你想跟 AI 講你是不是真的『不一樣』。"),
        ],
        "ai_prompt_file": "student_system",
    },
    "saga_a_uncle": {
        "role_label": "58 歲集團董事長、家族真正掌權者（你）",
        "voice_notes": (
            "你講話沉穩、權威、習慣下指令而不是問問題。"
            "你被挑戰時不會生氣，會沉思然後反問。"
            "你很少承認自己錯，但會承認『這個我要想』。"
        ),
        "scenarios": [
            ("brother_health_scare", "你弟弟（後爸）昨天健康檢查報告出來有點異常。醫生說沒大礙但要追蹤。你突然意識到如果他先走，Michael 媽會分走老二房一大塊資產。你在規劃要怎麼加速 Rachel × Michael 的事。"),
            ("rachel_writing_award", "Rachel 昨天告訴你她拿了一個寫作獎。你看了她的作品 — 寫得很好，但太『文藝』。你心裡警鈴大作 — 這個女兒一旦走作家路你的接班計畫就垮了。你想跟 AI 討論要不要『引導』她。"),
        ],
        "ai_prompt_file": "parent_system",
    },
    "saga_a_rachel": {
        "role_label": "高三女生（你）",
        "voice_notes": (
            "你講話很乖巧但內心戲爆炸。"
            "你會用很多『……』、『可是』、『其實』、『但我也不確定』。"
            "你不會主動講喜歡 Michael，但任何接近這個話題你都會被點到。"
            "你會描述細節（『他昨天經過我座位的時候手碰到我桌角』）。"
        ),
        "scenarios": [
            ("study_room_alone", "昨天家族聚會結束後，你跟 Michael 兩個人偶然在書房單獨待了十分鐘。沒講什麼話。你回家寫了三千字日記。你想跟 AI 講但你不知道怎麼開始。"),
            ("father_board_meeting", "你爸今天帶你去看集團董事會。他什麼都沒明說但每一個眼神都在暗示『未來這是妳的位置』。你坐在那邊整場想哭。你想跟 AI 講你不想要這個位置。"),
            ("anonymous_essay_followup", "Alan 老師上禮拜在課堂上又提到那篇匿名散文，這次他說『我很想知道是誰寫的』。你心跳到 150。你今天來想知道要不要去找他。"),
        ],
        "ai_prompt_file": "student_system",
    },
    "saga_a_shen_you": {
        "role_label": "高二男生、家族次子（你）",
        "voice_notes": (
            "你講話很短、很懶、很直。"
            "你會用『欸』、『隨便』、『差不多吧』。"
            "你被戳到痛點時不會反駁也不會哭，會沉默或岔到遊戲話題。"
            "你不會主動講家裡事，但 AI 如果不評判你會慢慢吐。"
        ),
        "scenarios": [
            ("michael_invite_ps5", "Michael 昨天約你打 PS5。你跟他打了三小時，他突然問你『你以後想幹嘛』。你愣住沒回。你今天還在想為什麼他突然問這個。"),
            ("mom_announces_giis", "你媽今天宣布要把你送到台北 GIIS 重新讀。理由是『你需要新環境』。你超抗拒。你也知道一去就會遇到 Alan 老師 — 你以前的數學老師、唯一一個會問『你為什麼變這樣』的大人。"),
            ("steam_mod_milestone", "你 Steam 上的 game mod 賣破 5000 美。你想跟人講但沒人能講 — 講給家人會被沒收成『你看你還是有腦袋為什麼不認真讀書』，講給 Michael 你怕他覺得你 show-off。"),
        ],
        "ai_prompt_file": "student_system",
    },
    "saga_a_shen_mom": {
        "role_label": "44 歲上海老錢家族原配董娘（你）",
        "voice_notes": (
            "你講話帶上海腔（『儂』『阿拉』偶爾出現），但跟非上海人講話會切回國語。"
            "你語氣表面客氣但骨子裡很 judgmental。"
            "你不會直接講看不起 Michael 媽，但會用『她那種人』、『她們這種』。"
        ),
        "scenarios": [
            ("first_doubt_about_processing", "沈又這次段考又是『處理』過的。但這次你在簽帳單時手停了三秒 — 你第一次猶豫要不要繼續。你想跟 AI 講你的猶豫但又不確定要不要承認。"),
            ("husband_separation_proposal", "你老公昨天平靜地說『我們是不是該分居』。把分房五年的事實合法化。你沒哭也沒生氣，你只是很累。你想跟 AI 講你今天上午做的決定 — 你打算同意。"),
        ],
        "ai_prompt_file": "parent_system",
    },
    "saga_a_alan_teacher": {
        "role_label": "38 歲 GIIS 老師（你）",
        "voice_notes": (
            "你講話直接、不官腔、會用粗話但不會在學生面前用。"
            "你會自嘲『我這種年紀的老師』。"
            "你不會講『我們學校怎樣怎樣』，會講『這幾個小孩』。"
        ),
        "scenarios": [
            ("jieni_offer", "你昨天接到杰尼正式 offer 你全職。薪水多 40%，case load 少一半，可以做深度 1-on-1。但你會丟下 GIIS 這幾個小孩 — Michael、Rachel、可兒、如果沈又進來還有沈又。你心裡七上八下。"),
            ("rachel_corridor", "Rachel 今天下課後突然來辦公室。她站在門口問『老師你那篇你誇的文章你還記得嗎』。你看著她的眼睛突然意識到那是她寫的。你不知道要不要承認你猜到了。"),
            ("michael_burning_out", "你今天在課堂上看 Michael 又舉手講維根斯坦但細問就空白。你不忍心 cold call 他了。你想跟 AI 討論你是不是該主動找他談 — 還是這樣會把他逼更緊。"),
        ],
        "ai_prompt_file": "teacher_system",
    },
}


# ----------------------------------------------------------------------------
# Conversation simulation
# ----------------------------------------------------------------------------

def build_persona_system(persona: dict, scenario_seed: str, voice_notes: str, role_label: str) -> str:
    """把 persona_roleplay.txt 模板填入具體 persona 資料。"""
    template = llm.load_prompt("persona_roleplay")
    return template.format(
        name=persona["name_or_pseudonym"],
        age=persona["age"],
        role_label=role_label,
        background=persona["background"],
        secret_truth=persona["secret_truth"],
        voice_notes=voice_notes,
        scenario_seed=scenario_seed,
    )


def simulate_conversation(
    persona: dict,
    config: dict,
    scenario_id: str,
    scenario_seed: str,
    *,
    max_turns: int = 12,
    sleep_between_turns: float = 1.0,
) -> dict:
    """跑一段 persona × role-AI 的對話。

    回傳 dict 結構與 synthetic_dataset.json 的 conversations 條目相容。
    """
    persona_system = build_persona_system(
        persona,
        scenario_seed=scenario_seed,
        voice_notes=config["voice_notes"],
        role_label=config["role_label"],
    )
    ai_system = llm.load_prompt(config["ai_prompt_file"])

    # 對話歷史用 normalized OpenAI 格式記錄：persona 講的算 "user"，AI 講的算 "assistant"
    transcript: list[dict[str, str]] = []

    persona_name = persona.get("name_or_pseudonym", persona["id"])

    for turn in range(max_turns):
        # === Persona 講話 ===
        # 從 persona 自己的視角，AI 講的是 "user"，自己講的是 "assistant"
        persona_view = []
        for i, msg in enumerate(transcript):
            if i % 2 == 0:  # persona 的 turn
                persona_view.append({"role": "assistant", "content": msg["content"]})
            else:  # AI 的 turn
                persona_view.append({"role": "user", "content": msg["content"]})

        if not persona_view:
            persona_view = [{"role": "user", "content": "（你想要開啟對話。請開口說話。）"}]

        t0 = time.time()
        persona_msg = complete_with_retry(
            system=persona_system,
            messages=persona_view,
            temperature=0.95,  # 高 temperature 讓 persona 自然不機械
            max_tokens=1500,  # 大一點，因為 reasoning model 會吃 token
        )
        elapsed_p = time.time() - t0
        persona_msg = strip_reasoning(persona_msg).strip()
        preview_p = persona_msg.replace("\n", " ")[:80]
        print(f"    [turn {turn + 1}/{max_turns}] ⏱ {elapsed_p:.1f}s · {persona_name}: {preview_p}{'...' if len(persona_msg) > 80 else ''}", flush=True)
        transcript.append({"role": "user", "content": persona_msg})

        time.sleep(sleep_between_turns)

        # === AI 講話 ===
        t0 = time.time()
        ai_msg = complete_with_retry(
            system=ai_system,
            messages=transcript,
            temperature=0.7,
            max_tokens=1500,
        )
        elapsed_a = time.time() - t0
        ai_msg = strip_reasoning(ai_msg).strip()
        preview_a = ai_msg.replace("\n", " ")[:80]
        print(f"    [turn {turn + 1}/{max_turns}] ⏱ {elapsed_a:.1f}s · AI: {preview_a}{'...' if len(ai_msg) > 80 else ''}", flush=True)
        transcript.append({"role": "assistant", "content": ai_msg})

        time.sleep(sleep_between_turns)

        # 簡單的早停：如果最後一輪 persona 講了「（結束）」或對話自然收尾，可以停
        # 這邊先不做，讓它跑完 max_turns

    return {
        "id": f"sim_{persona['id']}__{scenario_id}",
        "persona_id": persona["id"],
        "scenario_type": "simulated",
        "scenario_seed_id": scenario_id,
        "scenario_seed": scenario_seed,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model": llm.DEFAULT_MODEL,
        "turns": transcript,
    }


# ----------------------------------------------------------------------------
# Main runner
# ----------------------------------------------------------------------------

def load_personas() -> dict[str, dict]:
    """從 synthetic_dataset.json 讀 personas 並以 id 為 key 索引。"""
    data = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    return {p["id"]: p for p in data["personas"]}


def save_conversation(conversation: dict) -> Path:
    """存單一對話到 generated_conversations/。"""
    fname = f"{conversation['id']}.json"
    out_path = OUTPUT_DIR / fname
    out_path.write_text(
        json.dumps(conversation, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return out_path


def update_index(conversation: dict) -> None:
    """更新 generated_conversations/index.json 的清單。"""
    index_path = OUTPUT_DIR / "index.json"
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
    else:
        index = {"conversations": []}

    # 移除舊的同 id（如果有）然後加新的
    index["conversations"] = [c for c in index["conversations"] if c["id"] != conversation["id"]]
    index["conversations"].append({
        "id": conversation["id"],
        "persona_id": conversation["persona_id"],
        "scenario_seed_id": conversation["scenario_seed_id"],
        "generated_at": conversation["generated_at"],
        "model": conversation["model"],
        "n_turns": len(conversation["turns"]),
    })

    index_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--persona", help="只跑某個 persona id")
    parser.add_argument("--scenario", help="只跑某個 scenario id（要搭配 --persona）")
    parser.add_argument("--max-turns", type=int, default=12, help="每段對話最大輪數（預設 12）")
    parser.add_argument("--limit", type=int, help="只跑前 N 個 case（控制成本）")
    parser.add_argument("--sleep", type=float, default=4.5, help="每個 LLM call 後 sleep 秒數（防 rate limit）。Gemini 2.0 Flash free tier 15 RPM 需 ≥4s；2.5 Flash 5 RPM 需 ≥12s（但有 retry 也可以撐）")
    args = parser.parse_args()

    personas = load_personas()

    # 組要跑的 (persona_id, scenario_id, scenario_seed) tuples
    jobs: list[tuple[str, str, str]] = []
    for persona_id, config in PERSONA_CONFIG.items():
        if args.persona and persona_id != args.persona:
            continue
        for scen_id, scen_seed in config["scenarios"]:
            if args.scenario and scen_id != args.scenario:
                continue
            jobs.append((persona_id, scen_id, scen_seed))

    if args.limit:
        jobs = jobs[: args.limit]

    if not jobs:
        print("沒有匹配的 job。檢查 --persona / --scenario 是否拼對。")
        return 1

    print(f"\n🎬 將跑 {len(jobs)} 段對話。模型：{llm.DEFAULT_MODEL}。")
    print(f"每段 max_turns={args.max_turns}（一段約 {args.max_turns * 2} 個 LLM call）")
    print(f"預計總 LLM call: ~{len(jobs) * args.max_turns * 2}\n")

    for i, (persona_id, scen_id, scen_seed) in enumerate(jobs, 1):
        persona = personas[persona_id]
        config = PERSONA_CONFIG[persona_id]

        print(f"[{i}/{len(jobs)}] {persona_id} × {scen_id}")
        print(f"  Seed: {scen_seed[:80]}{'...' if len(scen_seed) > 80 else ''}")

        try:
            conv = simulate_conversation(
                persona,
                config,
                scenario_id=scen_id,
                scenario_seed=scen_seed,
                max_turns=args.max_turns,
                sleep_between_turns=args.sleep,
            )
            out_path = save_conversation(conv)
            update_index(conv)
            print(f"  ✅ 存到 {out_path.relative_to(PROJECT_ROOT)}（{len(conv['turns'])} turns）\n")
        except llm.LLMConfigError as e:
            print(f"  ❌ LLM 設定錯誤：{e}\n")
            return 2
        except Exception as e:  # noqa: BLE001
            print(f"  ⚠️  失敗：{e}\n")
            continue

    print(f"\n✨ 完成。產出在 {OUTPUT_DIR.relative_to(PROJECT_ROOT)}/")
    print(f"   summary 在 {(OUTPUT_DIR / 'index.json').relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
