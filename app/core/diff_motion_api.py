import requests
from typing import Dict, Any

BASE_URL = "http://localhost:37264"


# プリセットを切り替える
def switch_preset(preset_name: str) -> bool:
    url = f"{BASE_URL}/preset/switch"
    payload: Dict[str, Any] = {"name": preset_name}

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()

        data = response.json()
        if data.get("success"):
            print(f"プリセット切り替え成功: {preset_name}")
            return True
        else:
            print(f"APIエラー: {data.get('message')}")
            return False

    except Exception as e:
        print(f"エラー: プリセット切り替えに失敗しました: {e}")
        return False


# プリセットを取得する
def get_presets() -> list[str]:
    url = f"{BASE_URL}/presets"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        presets = []
        if data.get("success") and "windows" in data:
            for window in data["windows"]:
                for preset in window.get("presets", []):
                    presets.append(preset["name"])

        return sorted(list[str](set[str](presets)))

    except Exception as e:
        print(f"エラー: プリセットの取得に失敗しました: {e}")
        return []
