import os
import sys
import django
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), "/CareerCompass"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CareerCompassProject.settings')
django.setup()
from CCapp.models import Area1, Area2
from django.db import transaction

def makePath(fileName):
    csvFilePath='/CareerCompass/setup/csv/'
    filePath=os.path.join(os.path.dirname(__file__),f'{csvFilePath}{fileName}.csv')
    return filePath

def area0(filePath):
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            with transaction.atomic():
                for row in reader:
                    regionName = row['name']
                    Area1.objects.get_or_create(name=regionName)
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def area1(filePath):
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            with transaction.atomic():
                for row in reader:
                    region,prefecture = row['region'], row['name']
                    region, created = Area1.objects.get_or_create(name=region)
                    Area2.objects.create(name=prefecture, area0=region)
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def area2(filePath):
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)  # ヘッダー行をスキップ
            with transaction.atomic():  # トランザクションで一括処理
                for row in reader:
                    prefecture_name, city_name = row[0], row[1]
                    # Area1の都道府県が存在するか確認、なければ作成
                    prefecture, created = Area1.objects.get_or_create(name=prefecture_name)
                    # Area2に市区町村データを挿入
                    Area2.objects.create(name=city_name, area1=prefecture)
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def tag(filePath):
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            with transaction.atomic():  # トランザクションで一括処理
                for row in reader:
                    tagName = row['name']
                    Area1.objects.get_or_create(name=tagName)
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def category00(filePath):
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            with transaction.atomic():
                for row in reader:
                    tagName = row['name']
                    Area1.objects.get_or_create(name=tagName)
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 実行
fileList=[
    'area0',
    'area1',
    'area2',
    # 'category00',
    # 'category01',
    # 'category10',
    # 'category11',
    # 'corporation',
    # 'DM',
    # 'offer',
    # 'profile',
    # 'supportDM',
    'tag',
    # 'user',
]

pathList=[]

for i in fileList:
    pathList.append(makePath(i))

area0()
area1()
area2()
tag()
