import csv
from django.core.exceptions import ObjectDoesNotExist
from django_setup_def import djangoImportSetup
djangoImportSetup()
from CCapp.models import *
from CCapp.defs import *

# CSVファイルにデータを書き込む
filename = 'job_listings.csv'

# CSVのヘッダー
headers = [
    "name", "detail", "solicitation", "course", "forms", "roles", "CoB", 
    "subject", "NoP", "departments", "characteristic", "PES", "giving", 
    "allowances", "salaryRaise", "bonus", "holiday", "welfare", "workingHours", 
    "area1name", "category00name", "category01name", "category10name", 
    "category11name", "corporationID", "applicants", "period", "status"
]

# Offerのオブジェクトを取得
offers = Offer.objects.all()

# ファイルを開いて書き込む
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    
    # ヘッダーを書き込む
    writer.writeheader()

    # Offerデータを書き込む
    for offer in offers:
        try:
            # 外部キーが関連するオブジェクトのIDを取得
            welfare_id = offer.welfare.id if offer.welfare else None
            area1_name = offer.area1.name if offer.area1 else None
            category00_name = offer.category00.name if offer.category00 else None
            category01_name = offer.category01.name if offer.category01 else None
            category10_name = offer.category10.name if offer.category10 else None
            category11_name = offer.category11.name if offer.category11 else None
            corporation_id = offer.corporation.id if offer.corporation else None
            
            # ManyToManyField（応募者リスト）は、ユーザーIDをカンマ区切りで書き込む
            applicants_ids = ', '.join([str(user.id) for user in offer.applicants.all()])

            # データを辞書として構成
            row = {
                "name": offer.name, 
                "detail": offer.detail, 
                "solicitation": offer.solicitation, 
                "course": offer.course, 
                "forms": offer.forms, 
                "roles": offer.roles, 
                "CoB": offer.CoB, 
                "subject": offer.subject, 
                "NoP": offer.NoP, 
                "departments": offer.departments, 
                "characteristic": offer.characteristic, 
                "PES": offer.PES, 
                "giving": offer.giving, 
                "allowances": offer.allowances, 
                "salaryRaise": offer.salaryRaise, 
                "bonus": offer.bonus, 
                "holiday": offer.holiday, 
                "welfare": welfare_id,  # WelfareのIDを挿入
                "workingHours": offer.workingHours, 
                "area1name": area1_name,  # Area1の名前を挿入
                "category00name": category00_name,  # カテゴリ名を挿入
                "category01name": category01_name, 
                "category10name": category10_name, 
                "category11name": category11_name, 
                "corporationID": corporation_id,  # 法人IDを挿入
                "applicants": applicants_ids,  # 応募者のIDリストを挿入
                "period": offer.period.strftime('%Y-%m-%d %H:%M:%S'),  # 日付を文字列に変換
                "status": offer.status,  # 公開状況
            }
            
            # データを書き込む
            writer.writerow(row)
        except ObjectDoesNotExist as e:
            print(f"Error processing offer {offer.id}: {e}")

print(f"Data has been written to {filename}.")
