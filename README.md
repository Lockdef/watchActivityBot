# watchAcitivyBot

Discord ユーザーのアクティビティを Twitter のプロフィールにリアルタイムで同期させる Bot 及び Web アプリケーション

## 環境構築

```
pip install requirements.txt
```

## 起動方法

Web サーバー起動

```
python app.py
```

DiscordBot 起動

```
python bot.py
```

## 使用技術

| 名前        | 概要                           |
| ----------- | ------------------------------ |
| Python3.8.2 | プログラミング言語             |
| Flask       | Web バックエンドフレームワーク |
| SQLAlchemy  | SQL/sqlite3 の Wrapper         |
| Tweepy      | TwitterAPI の Wrapper          |
| Discord.py  | DiscordAPI の Wrapper          |
| Heroku      | Hosting サービス               |

## DB 周りについて

- DB ファイル名は`./user.db`
- DB のモデル定義は`/models`
- DB のロジック定義は`/repositories`

## CSS 周りについて

- 変数は`:root`で全て定義する
- 最低でもカラーコードは全て変数化する
