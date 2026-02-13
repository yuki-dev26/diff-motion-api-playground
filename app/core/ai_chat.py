import os
import re
from fastapi import HTTPException
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from app.api.models import ChatResponse
from app.core.diff_motion_api import switch_preset

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEYが設定されていません")
        _client = OpenAI(api_key=api_key)
    return _client


async def chat_with_ai(
    message: str, system_prompt: str, available_presets: list[str]
) -> ChatResponse:
    try:
        client = get_client()

        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ]

        response = client.chat.completions.create(
            model="gpt-4.1-mini", messages=messages
        )

        content = response.choices[0].message.content
        if not content:
            raise HTTPException(status_code=500)

        emotion_match = re.search(r"\[\[(.*?)\]\]", content)
        emotion = ""
        clean_content = content

        if emotion_match:
            emotion = emotion_match.group(1)
            clean_content = content.replace(emotion_match.group(0), "").strip()

            if emotion in available_presets:
                success = switch_preset(emotion)
                if not success:
                    print(f"エラー: プリセット切り替えに失敗しました: {emotion}")

        return ChatResponse(content=clean_content, emotion=emotion)

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
