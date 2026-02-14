# Diff Motion API Playground

![Tech Stack](https://skillicons.dev/icons?i=html,css,js,py,fastapi&perline=8)

Diff Motion APIと連携して、AIの回答に応じてキャラクターの表情(ポーズ等)を切り替えるデモアプリケーション

![image](https://github.com/user-attachments/assets/24461c3c-93c2-4358-9d1c-20f1642caa46)

> [!IMPORTANT]
> 本デモの動作には、[Diff Motion](https://yuki-p.booth.pm/items/7913743)の購入が必要です。

<!-- -->

> [!TIP]
> Diff Motion APIについては、[こちらの記事](https://note.com/yuki_tech/n/nd4425bdbef65)を併せてご覧ください。

## プロジェクト構造

```text
app/
├── api/                    # APIエンドポイント関連
│   ├── models.py          # リクエスト/レスポンスモデル
│   └── routes.py          # ルート定義
├── core/                   # コアロジック
│   ├── __init__.py
│   ├── ai_chat.py         # AIチャット機能
│   └── diff_motion_api.py # Diff Motion API連携
├── config/                 # 設定ファイル
│   └── system_prompt.md   # システムプロンプト
├── static/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── favicon.ico
└── main.py
```

## 🚀 セットアップ

### 0. uv のインストール (未インストールの場合)

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. リポジトリのクローン

```bash
git clone https://github.com/yuki-dev26/diff-motion-api-playground.git
cd diff-motion-api-playground
```

### 2. 環境変数の設定

`.env` ファイルを作成し、OpenAI API キーを設定してください。

```bash
OPENAI_API_KEY="your_api_key"
```

> [!TIP]
> OpenAI APIキーの取得方法については、[こちらの記事](https://note.com/yuki_tech/n/nbc29be8da07f)を参照してください。

### 3. 依存関係のインストール

```bash
uv sync
```

### 4. アプリケーションの起動

以下のコマンドでサーバーを起動します。

```powershell
uv run python -m app.main
```

ブラウザで [http://localhost:8000](http://localhost:8000) を開く

### 5. APIドキュメント

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 使い方

1. **Diff Motionの起動**
   - Diff Motionアプリケーションを起動してください
   - プリセットに名前を入力する(感情分類のキーワードとなる)
   - APIサーバーが自動的に起動します（デフォルト: `http://localhost:37264`）

2. **プリセットの取得と切り替えについて**
   - Diff Motion API Playgroundが開いたらDiff Motionに登録済みのプリセット名が表示される
   - プリセット名をクリックするとそのプリセットに切り替わります

3. **チャットによるプリセット切り換え**
   - Diff Motion API Playgroundを起動後にブラウザで `http://localhost:8000` にアクセス
   - チャット欄にメッセージを入力して送信
   - AIが応答し、その感情に応じてDiff Motionのプリセットが自動的に切り替わります

## 🔧 プリセット切り替えの仕組み

1. **プリセット取得**: アプリ起動時にDiff Motion APIからプリセット名を取得し、システムプロンプトに動的注入
2. **システムプロンプト**: AIに `[[感情]]` タグを応答に含めるよう指示（使用可能なプリセット名のリストも含む）
3. **タグ抽出**: 正規表現 `\[\[(.*?)\]\]` でAI応答からタグを抽出
4. **プリセット切り替え**: タグ内容がDiff Motionのプリセット名と一致すれば `http://localhost:37264/preset/switch` にPOSTリクエストを送信

## Supporters

[![note メンバーシップ](https://img.shields.io/badge/note-Membership-41C9B4?style=for-the-badge&logo=note&logoColor=white)](https://note.com/yuki_tech/membership/members)

## License

Copyright (c) 2026 [yuki-P](https://x.com/yuki_p02)
Licensed under the [MIT License](LICENSE).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
