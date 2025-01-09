import os
import logging
import datetime
from django_setup_def import djangoImportSetup
djangoImportSetup()
from CCapp.models import *
from CCapp.defs import makeDirFile,makeImportPath,logconfig,logException,logsOutput,readFile,executeFunction
from django.db import transaction
import csv
import random
from itertools import cycle  # 無限ループでデータを扱うためのモジュール

# CSVファイルから指定カラム（name）を読み込む関数
def load_csv_column(file_path, column_name="name"):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row[column_name] for row in reader if column_name in row]
    
# CSVファイルから指定カラム（name）を読み込む関数
def load_cId_column(file_path, column_name="cId"):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row[column_name] for row in reader if column_name in row]

# 外部CSVファイルからデータを読み込む
area1names = cycle(load_csv_column("setup/data/area1.csv"))
category00names = cycle(load_csv_column("setup/data/category00.csv"))  # 会社種別
category01names = cycle(load_csv_column("setup/data/category01.csv"))  # 会社規模
category10names = cycle(load_csv_column("setup/data/category10.csv"))  # 会社形態
category11names = cycle(load_csv_column("setup/data/category11.csv"))  # 会社業種
corporationIDs = cycle(load_cId_column("setup/data/corporation.csv"))  # 会社ID

# 固定データ
fixed_data = {
    "workingHours": "8時間",
    "period": "2025-05-12 12:15:20",
    "status": True,
    "detail": "あいうえお",
    "PES": "かきくけこ",
    "salaryRaise": "年2回",
    "bonus": "基本給6か月分",
    "allowances": "家賃手当",
}

# 出力ファイルのパス
output_file = "offer.csv"

# ヘッダー定義
header = [
    "title", "giving", "holiday", "area1name",
    "category00name", "category01name", "category10name", "category11name", "corporationID",
    "workingHours", "period", "status", "detail", "PES", "salaryRaise", "bonus", "allowances"
]

# CSVファイルを初期化（ヘッダーを書き込み）
with open(output_file, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()

# データを都度生成して書き込む
with open(output_file, mode="a", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=header)

    for i in range(1, 400000):  # 40万件生成
        row = {
            "title": f"求人{i:06d}",
            "giving": random.randint(150000, 300000),  # 給料
            "holiday": random.randint(100, 140),  # 休日
            "area1name": next(area1names),  # 都道府県（順に利用）
            "category00name": next(category00names),  # 会社種別（順に利用）
            "category01name": next(category01names),  # 会社規模（順に利用）
            "category10name": next(category10names),  # 会社形態（順に利用）
            "category11name": next(category11names),  # 会社業種（順に利用）
            "corporationID": next(corporationIDs),  # 会社ID
        }
        row.update(fixed_data)  # 固定データを追加
        writer.writerow(row)  # CSVに追記

        # プログレス表示（任意）
        if i % 10000 == 0:
            print(f"{i}件のデータを生成・書き込み済み")

print(f"データを {output_file} に書き出しました！")