# ews
Enpit Web Service(仮)

# 機能
サーバ上に仮想マシンを作成、操作、削除できる。

# 開発ルール
1. 作業前にはredmineでticket作成
2. gitで作業ブランチを切る(masterでは作業しない)
3. 事前に、slackにこれから行う作業内容を投稿
4. こまめに作業ブランチにプッシュする
5. mergeしたいときはプルリクエストを作成(`https://github.com/tomoasleep/ews/compare/[ブランチ名]`)
6. 返答を待つ

## 注意点
* 各コミットが何をしているのか分かるように、作業内容は細かく分割してください。


# 注意
## 開発環境
`ews/settings/dev.py.local` に設定ファイルのひな形があるので、これを `dev.py` にリネームして、中のシークレットキーを適当に変更してください。

## 本番環境
`ews/settings/production.py.local` に設定ファイルのひな形があるので、これを `production.py` にリネームして、中のシークレットキーを適当に変更してください。

# 環境設定
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
# パスワード等の設定を行う
```

## 本番環境
(`libvirt`のインストールが必要)

```bash
pip install -r requirements_production.txt
```

# 起動
## 開発環境
`python manage.py runserver` (python 2系とdjango 1.8系が必要)

dev環境では libvirt系のモジュールを使わなくなる。

## 本番環境
`PRODUCTION=y python manage.py runserver` (python 2系とdjango 1.8系が必要)
