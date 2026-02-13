from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from app.api.models import ChatRequest, ChatResponse
from app.core.ai_chat import chat_with_ai
from app.core.diff_motion_api import switch_preset

BASE_DIR = Path(__file__).resolve().parent.parent

router = APIRouter()

available_presets = []
current_system_prompt = ""


def set_state(presets: list[str], prompt: str):
    global available_presets, current_system_prompt
    available_presets = presets
    current_system_prompt = prompt


@router.get("/")
async def read_root():
    return FileResponse(BASE_DIR / "static/index.html")


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(BASE_DIR / "favicon.ico")


@router.get("/emotions")
async def get_emotions():
    return {"emotions": available_presets}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return await chat_with_ai(request.message, current_system_prompt, available_presets)


@router.post("/switch_preset")
async def api_switch_preset(request: ChatRequest):
    try:
        preset_name = request.message
        if preset_name in available_presets:
            success = switch_preset(preset_name)
            if success:
                return {"status": "success", "preset": preset_name}
            else:
                raise HTTPException(
                    status_code=500, detail="プリセット切り替えに失敗しました"
                )
        else:
            raise HTTPException(status_code=400, detail="不明なプリセット名です")
    except Exception as e:
        print(f"Error switching preset: {e}")
        raise HTTPException(status_code=500, detail=str(e))
