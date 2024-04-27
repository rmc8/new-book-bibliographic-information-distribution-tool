# 新刊書籍情報収集ツール

このツールは、国立国会図書館サーチAPIを利用して、新刊書籍情報を収集し、DiscordのWebhookにて通知を行うPythonスクリプトです。

## 機能

- 指定されたキーワードに合致する新刊書籍情報を収集
- 収集した書籍情報をDiscordのWebhookにサイレントメッセージとして通知
- 通知済みの書籍情報をSQLiteデータベースに記録し、重複通知を防止

## 使用方法

1. 必要なパッケージをインストールします。

```
pip install -r requirements.txt
```

2. `settings.yaml`ファイルを編集し、検索キーワードとDiscordのWebhookURLを設定します。

```yaml
keywords:
  - Python
discord:
  webhook: "https://discord.com/api/webhooks/..."
```

3. スクリプトを実行します。

```
python src/main.py
```

## ディレクトリ構造

```
📦新刊書籍情報収集ツール
 ┣ 📂src
 ┃ ┣ 📂libs
 ┃ ┃ ┣ 📂model
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┗ 📜book_data.py
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜db.py
 ┃ ┃ ┣ 📜ndl.py
 ┃ ┃ ┗ 📜report.py
 ┃ ┣ 📜main.py
 ┃ ┗ 📜settings.yaml
 ┣ 📜.gitignore
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┗ 📜books.db
```

- `src/`: ソースコードが格納されているディレクトリ
  - `libs/`: ライブラリモジュールが格納されているディレクトリ
    - `model/book_data.py`: 書籍データモデルの定義
    - `db.py`: SQLiteデータベースの操作を行うモジュール
    - `ndl.py`: 国立国会図書館サーチAPIの操作を行うモジュール
    - `report.py`: DiscordのWebhookへの通知を行うモジュール
  - `main.py`: メインスクリプト
  - `settings.yaml`: 設定ファイル
- `requirements.txt`: 必要なパッケージの一覧
- `books.db`: 通知済みの書籍情報を格納するSQLiteデータベース

## 注意事項

- Discordのサーバー側で、Webhookの設定が適切に行われている必要があります。
- 大量のリクエストを送信すると、国立国会図書館サーチAPIからブロックされる可能性があります。キーワードを多量に含む場合には`sleep`の値を延ばすなどして十分なリクエスト間隔を確保してください。

## ライセンス

- このプロジェクトは[MITライセンス](./LICENCE)の下で公開されています。
- 本サービスで提供するのメタデータの一部は、国立国会図書館サーチのAPIに由来します。ライセンスは[クリエイティブ・コモンズ 表示 4.0 国際 パブリック・ライセンス](https://creativecommons.org/licenses/by/4.0/legalcode.ja)です。
