import requests
from typing import Any, Dict

BASE_URL = "http://localhost:37264"


# プリセットを切り替える
def switch_preset():
    print("--- プリセット切り替え ---")

    # プリセット名の入力
    preset_name = input("切り替え先のプリセット名を入力してください: ").strip()

    if not preset_name:
        print("エラー: プリセット名が入力されていません。処理を中止します。")
        return

    payload: Dict[str, Any] = {"name": preset_name}

    url = f"{BASE_URL}/preset/switch"

    try:
        print(f"\nリクエストを送信中...: {url}")
        response = requests.post(url, json=payload)

        response.raise_for_status()

        data = response.json()

        if data.get("success"):
            print(f"メッセージ: {data.get('message')}")
        else:
            print("APIエラー (success=false):", data)

    except requests.exceptions.ConnectionError:
        print("エラー: Diff Motionが起動しているか確認してください。")
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    switch_preset()
