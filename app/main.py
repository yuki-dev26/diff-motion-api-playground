import re
import uvicorn
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.api import routes
from app.core.diff_motion_api import get_presets

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

available_presets = []
base_system_prompt = ""
current_system_prompt = ""


def update_presets():
    global available_presets, current_system_prompt
    available_presets = get_presets()
    if not available_presets:
        print("エラー: プリセットが見つかりません")

    preset_tags = ", ".join([f"[[{p}]]" for p in available_presets])
    marker = "使用可能な感情タグ"

    if marker in base_system_prompt:
        pattern = rf"(?s)({re.escape(marker)}).*?(\n\s*\n|\Z)"
        current_system_prompt = re.sub(
            pattern, rf"\1\n{preset_tags}\2", base_system_prompt, count=1
        )
    else:
        current_system_prompt = f"{base_system_prompt}\n\n{marker}\n{preset_tags}"

    routes.set_state(available_presets, current_system_prompt)


@asynccontextmanager
async def lifespan(_: FastAPI):
    global base_system_prompt

    try:
        with open(BASE_DIR / "config/system_prompt.md", "r", encoding="utf-8") as f:
            base_system_prompt = f.read().strip()
    except FileNotFoundError:
        print("エラー: システムプロンプトファイルが見つかりません")

    update_presets()

    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(routes.router)


@app.post("/update_presets")
async def api_update_presets():
    update_presets()
    return {"status": "success", "emotions": available_presets}


if __name__ == "__main__":

    print("Starting server...")
    print("Access the playground at: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
