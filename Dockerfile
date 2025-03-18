# Python 3.12 の軽量イメージを使用
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新と必要なライブラリのインストール
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコンテナにコピー
COPY . .

# マイグレーションと静的ファイルの収集
RUN python manage.py migrate
RUN python setup/py/import_data.py
RUN python manage.py collectstatic --noinput

# Gunicorn でアプリケーションを起動
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "CareerCompassProject.wsgi:application"]
