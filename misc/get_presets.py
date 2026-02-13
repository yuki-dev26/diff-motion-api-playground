import requests

BASE_URL = "http://localhost:37264"


# 起動中のプリセット情報を取得する
def get_presets():
    url = f"{BASE_URL}/presets"

    try:
        print(f"リクエストを送信中...: {url}")
        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        if data.get("success"):

            print("\n--- プリセット一覧 ---")
            for window in data.get("windows", []):
                window_id = window.get("windowId")
                print(f"\n[Window {window_id}]")

                for preset in window.get("presets", []):
                    print(f"  - Name: {preset.get('name')} (ID: {preset.get('id')})")
        else:
            print("APIエラー (success=false):", data)

    except requests.exceptions.ConnectionError:
        print("エラー: Diff Motionが起動しているか確認してください。")
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    get_presets()
