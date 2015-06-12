# ews
Enpit Web Service(仮)

# 注意
`ews/settings/dev.py.local` に設定ファイルのひな形があるので、これを `dev.py` にリネームして、中のシークレットキーを適当に変更してください。

# 環境設定
(今はローカルで動かすのに`libvirt`のインストールが必要)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
# パスワード等の設定を行う
```

# 起動
`python manage.py runserver` (python 2系とdjango 1.8系が必要)
