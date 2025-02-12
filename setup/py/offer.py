import os
from django_setup_def import djangoImportSetup
djangoImportSetup()
from CCapp.models import *
from CCapp.defs import *
import logging
import random


djangoSetup()

# 固定データ
fixed_data = {
    "workingHours": "8時間",
    "period": "2025-05-12 12:15:20",
    "status": True,
    "detail": "業界をリードする技術を提供する弊社では、ソフトウェアエンジニアを募集しています。主な業務内容は、新規および既存のソフトウェアプロジェクトの設計、開発、およびメンテナンスを担当し、クライアントの要件を分析して最適なソリューションを提案することです。応募資格として、コンピュータサイエンスや情報技術に関する学位または実務経験が求められます。年俸は500万円以上で、正社員としての雇用形態です。詳細な情報は履歴書および職務経歴書を添付してお送りください。締め切りは2025年3月31日です。",
    "PES": "採用後の対応",
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

# ヘッダー定義
header = [
    "title", "giving", "holiday", "area1name",
    "category00name", "category01name", "category10name", "category11name", "corporationID",
    "workingHours", "period", "status", "detail", "PES", "salaryRaise", "bonus", "allowances",
    "solicitation", "course", "forms", "roles", "CoB", "subject", "NoP", "departments", "characteristic"
]

# 新しい追記用関数

def writeFileA(filePath, data):
    """追記用のCSV書き込み関数"""
    try:
        with open(filePath, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            if os.stat(filePath).st_size == 0:  # ファイルが空の場合はヘッダーを書き込み
                writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f'error in writeFileA: {e}')

# 入力ファイルパス生成
try:
    area1_path = makeImportPath("../setup/data/", "area1.csv")
    category00_path = makeImportPath("../setup/data/", "category00.csv")
    category01_path = makeImportPath("../setup/data/", "category01.csv")
    category10_path = makeImportPath("../setup/data/", "category10.csv")
    category11_path = makeImportPath("../setup/data/", "category11.csv")
    corporation_path = makeImportPath("../setup/data/", "corporation.csv")

    # CSVデータの読み込み
    area1names = [row['name'] for row in readFile(area1_path)]
    category00_map = {row['name']: [] for row in readFile(category00_path)}
    category10_map = {row['name']: [] for row in readFile(category10_path)}
    
    for row in readFile(category01_path):
        if row['category00name'] in category00_map:
            category00_map[row['category00name']].append(row['name'])
    
    for row in readFile(category11_path):
        if row['category10name'] in category10_map:
            category10_map[row['category10name']].append(row['name'])
    
    corporationIDs = [row['cId'] for row in readFile(corporation_path)]

    # 出力ファイル
    output_file = "offer.csv"

    # データ生成とCSV書き込み
    def generate_and_write_data():
        count = 1
        data = []
        for area in area1names:
            for category00, category01_list in category00_map.items():
                for category01 in category01_list:
                    for category10, category11_list in category10_map.items():
                        for category11 in category11_list:
                            corp_id = random.choice(corporationIDs)  # corporationIDs からランダム選定
                            row = {
                                "title": f"求人{count:06d}",
                                "giving": random.randint(150000, 300000),
                                "holiday": random.randint(100, 140),
                                "area1name": area,
                                "category00name": category00,
                                "category01name": category01,
                                "category10name": category10,
                                "category11name": category11,
                                "corporationID": corp_id,
                            }
                            row.update(fixed_data)
                            data.append(row)
                            count += 1

                            if count % 1000 == 0:
                                print(f"{count}件のデータを生成中...")

                            # プログレス表示（10,000件ごと）
                            if count % 10000 == 0:
                                logging.info(f"{count}件のデータを生成・書き込み済み")

                            # 一定量生成ごとに書き込み
                            if len(data) >= 1000:
                                writeFileA(output_file, data)
                                data = []

        # 最後のデータを書き込み
        if data:
            writeFileA(output_file, data)

    # 実行時間計測
    elapsed_time, _ = measureExecutionTime(generate_and_write_data)
    logging.info(f"データ生成処理完了: {elapsed_time:.2f}秒")

except Exception as e:
    logException(logging.getLogger(__name__), "データ生成エラー", e)
