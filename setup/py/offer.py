import os
import logging
import datetime
from django_setup_def import djangoImportSetup
djangoImportSetup()
from CCapp.models import *
from CCapp.defs import makeDirFile, makeImportPath, logconfig, logException, logsOutput, readFile, executeFunction
from django.db import transaction
import csv
import random
from itertools import cycle  # 無限ループでデータを扱うためのモジュール

# CSVファイルから指定カラム（name）を読み込む関数
def load_csv_column(file_path, column_name="name"):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row[column_name] for row in reader if column_name in row]

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
    "solicitation": "募集要項",
    "course": "コース名",
    "forms": "雇用形態",
    "roles": "配属職種",
    "CoB": "提出書類",
    "subject": "募集対象",
    "NoP": "募集人数",
    "departments": "募集学部",
    "characteristic": "募集特徴",
}

# 出力ファイルのパス
output_file = "offer.csv"

# ヘッダー定義
header = [
    "title", "giving", "holiday", "area1name",
    "category00name", "category01name", "category10name", "category11name", "corporationID",
    "workingHours", "period", "status", "detail", "PES", "salaryRaise", "bonus", "allowances",
    "solicitation", "course", "forms", "roles", "CoB", "subject", "NoP", "departments", "characteristic"
]

# **ファイルを開いた状態でループを回す**
with open(output_file, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()  # **ヘッダーの書き込み**

    count = 1
    # 多重ループ処理
    for area in area1names:
        for category00 in category00names:
            for category01 in category01names:
                for category10 in category10names:
                    for category11 in category11names:
                        for corp_id in corporationIDs:
                            row = {
                                "title": f"求人{count:06d}",
                                "giving": random.randint(150000, 300000),  # 給料
                                "holiday": random.randint(100, 140),  # 休日
                                "area1name": area,  # 都道府県
                                "category00name": category00,  # 会社種別
                                "category01name": category01,  # 会社規模
                                "category10name": category10,  # 会社形態
                                "category11name": category11,  # 会社業種
                                "corporationID": corp_id,  # 会社ID
                            }
                            row.update(fixed_data)  # **固定データを追加**
                            writer.writerow(row)  # **CSVに書き込む**
                            count += 1

        # プログレス表示（10,000件ごと）
        if count % 10000 == 0:
            print(f"{count}件のデータを生成・書き込み済み")

print(f"データを {output_file} に書き出しました！")
