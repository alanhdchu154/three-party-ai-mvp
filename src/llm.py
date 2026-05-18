"""LLM wrapper（透過 LiteLLM 當 universal adapter）。

設計選擇：
- 用 litellm.completion 而不是直接綁某一家 SDK——切換 provider 只需要改 .env
  的 `LLM_MODEL`，不需要改程式碼
- 預設 `gemini/gemini-2.5-flash`（Gemini Flash 免費額度夠開發用）
- API key 各 provider 各自的 env var（LiteLLM 會自動讀對應的）
- 友善錯誤訊息：找不到 key 時不要噴 traceback，而是告訴使用者該怎麼設

支援的 model 字串範例（更多看 https://docs.litellm.ai/docs/providers）：
- gemini/gemini-2.5-flash             需要 GEMINI_API_KEY
- gemini/gemini-2.5-pro               需要 GEMINI_API_KEY
- anthropic/claude-sonnet-4-5         需要 ANTHROPIC_API_KEY
- deepseek/deepseek-chat              需要 DEEPSEEK_API_KEY
- groq/llama-3.3-70b-versatile        需要 GROQ_API_KEY
- ollama/llama3.2                     本地不需要 key（先跑 `ollama serve`）
- openai/gpt-4o-mini                  需要 OPENAI_API_KEY
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# 載入 .env（如果存在）
load_dotenv()

DEFAULT_MODEL = os.getenv("LLM_MODEL", "gemini/gemini-2.5-flash")
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

# Model prefix → 對應的 env var。用於檢查使用者有沒有把對應的 key 設好。
_PROVIDER_KEY_MAP = {
    "gemini": "GEMINI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "groq": "GROQ_API_KEY",
    "openai": "OPENAI_API_KEY",
    "azure": "AZURE_API_KEY",
    "mistral": "MISTRAL_API_KEY",
    "cohere": "COHERE_API_KEY",
    "together_ai": "TOGETHERAI_API_KEY",
}


class LLMConfigError(Exception):
    """API key 沒設、模型錯誤等可預期的設定問題。"""


class LLMOutputError(Exception):
    """LLM 回傳的內容不符合期待（例如該回 JSON 卻回了一堆英文）。"""


def _provider_of(model: str) -> str:
    """取 model 字串的 provider 前綴（gemini/gemini-2.5-flash → gemini）。"""
    if "/" in model:
        return model.split("/", 1)[0].lower()
    # 沒前綴的視為 openai（litellm 預設行為）
    return "openai"


def _check_key_for(model: str) -> None:
    """檢查當前模型對應的 API key 是否已設好。Ollama 本地不需要。"""
    provider = _provider_of(model)
    if provider == "ollama":
        return  # 本地跑，不需要 key

    key_name = _PROVIDER_KEY_MAP.get(provider)
    if not key_name:
        # 未知 provider 不擋——讓 litellm 自己回錯誤
        return

    val = os.getenv(key_name, "")
    if not val or val.startswith("your-") or val.startswith("sk-ant-xxxxxxxx"):
        raise LLMConfigError(
            f"找不到 {key_name}（model = {model} 需要這個）。\n"
            f"請編輯 .env 並填入你的 key。\n"
            f"如果你想換 provider，把 .env 裡的 LLM_MODEL 改成別的（例如 "
            f"ollama/llama3.2 本地跑、deepseek/deepseek-chat 等）。"
        )


def _import_litellm():
    """惰性 import litellm（套件較大，啟動時 import 會慢）。"""
    try:
        import litellm
    except ImportError as e:
        raise LLMConfigError(
            "找不到 litellm 套件，請先執行：pip install -r requirements.txt"
        ) from e
    # 讓 litellm 安靜一點（不要每次都印 debug log）
    litellm.suppress_debug_info = True
    return litellm


def load_prompt(name: str) -> str:
    """從 prompts/ 讀檔。name 不用加 .txt。"""
    path = PROMPTS_DIR / f"{name}.txt"
    if not path.exists():
        raise FileNotFoundError(f"找不到 prompt 檔：{path}")
    return path.read_text(encoding="utf-8").strip()


def complete(
    system: str,
    messages: list[dict[str, str]],
    *,
    model: str | None = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> str:
    """呼叫 LLM（透過 LiteLLM），回傳純文字。

    `messages` 是 [{"role": "user"/"assistant", "content": "..."}, ...]。
    system prompt 會自動 prepend 成第一個 system message。
    """
    model = model or DEFAULT_MODEL
    _check_key_for(model)

    litellm = _import_litellm()

    # LiteLLM 接 OpenAI 格式：system 用 role=system 放第一筆
    full_messages: list[dict[str, str]] = [{"role": "system", "content": system}]
    full_messages.extend(messages)

    try:
        resp = litellm.completion(
            model=model,
            messages=full_messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    except Exception as e:
        raise LLMConfigError(f"呼叫 {model} 失敗：{e}") from e

    try:
        text = resp.choices[0].message.content  # type: ignore[union-attr]
    except (AttributeError, IndexError, KeyError) as e:
        raise LLMOutputError(f"LLM 回應結構異常：{resp}") from e

    if not text:
        raise LLMOutputError("LLM 沒有回傳任何 text content。")
    return text


def complete_json(
    system: str,
    messages: list[dict[str, str]],
    *,
    model: str | None = None,
    max_tokens: int = 1500,
    temperature: float = 0.3,
) -> dict[str, Any]:
    """呼叫 LLM 並解析 JSON。容錯：自動剝掉 ```json 包裝。"""
    raw = complete(
        system=system,
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return parse_json_lenient(raw)


def parse_json_lenient(raw: str) -> dict[str, Any]:
    """容錯 JSON 解析。處理：
    - 包在 ```json ... ``` 裡的
    - 前後有多餘文字的
    - 結尾少 } 的（盡量補）
    """
    text = raw.strip()

    # 剝掉 markdown code fence
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()

    # 找第一個 { 到最後一個 }
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise LLMOutputError(
            f"LLM 回應裡找不到 JSON 物件。原始回應：\n{raw[:500]}"
        )
    candidate = text[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        raise LLMOutputError(
            f"JSON 解析失敗（{e}）。原始回應：\n{raw[:500]}"
        ) from e
