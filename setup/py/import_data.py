import csv
from CCapp.models import Area1,Area2
from django.db import transaction

area1_csv_file_path='../csv/prefectures.csv'
area2_csv_file_path='../csv/municipalities.csv'

def area1():
    with open(area1_csv_file_path,newline='',encoding='utf-8') as csvfile:
        reader=csv.DictReader(csvfile)

    with transaction.atomic():  # トランザクションで一括処理
        for row in reader:
            prefecture_name=row['name']

            # Area1に都道府県データを追加
            Area1.objects.get_or_create(name=prefecture_name)

def area2():
    with open(area2_csv_file_path,newline='',encoding='utf-8') as csvfile:
        reader=csv.reader(csvfile)
        next(reader)  # ヘッダー行をスキップ

    with transaction.atomic():  # トランザクションで一括処理
        for row in reader:
            prefecture_name,city_name=row[1],row[2]

            # Area1の都道府県が存在するか確認、なければ作成
            prefecture,created=Area1.objects.get_or_create(name=prefecture_name)

            # Area2に市区町村データを挿入
            Area2.objects.create(name=city_name, area1=prefecture)