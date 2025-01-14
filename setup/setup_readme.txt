1.リポジトリのクローン

git clone https://github.com/ktq2390330/CareerCompass
cd CareerCompass

2.仮想環境のセットアップ
python -m venv myvenv
myvenv\Scripts\activate

3.パッケージのインストール
pip install -r requirements.txt

4.DBの設定
mysqlをダウンロードする(port:3307,name:root,password:password)
DBを作成(name:careercompassdb,host:127.0.0.1)
※DB設定を変更したい場合(その他の設定の変更や追加も可): python setup/py/change_setting.py
python setup/py/import_data.py

5.envファイルの作成
touch .env
以下の項目を設定
GEMINI_API_KEY
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD