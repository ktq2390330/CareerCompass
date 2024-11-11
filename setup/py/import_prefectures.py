import csv
from CCapp.models import Area1
from django.db import transaction

# CSVファイルのパスを指定
csv_file_path = '../csv/prefectures.csv'

# CSVデータのインポート
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    with transaction.atomic():  # トランザクションで一括処理
        for row in reader:
            prefecture_name = row['name']

            # Area1に都道府県データを追加
            Area1.objects.get_or_create(name=prefecture_name)
