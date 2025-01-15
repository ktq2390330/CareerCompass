import os
import logging
import datetime
from django_setup_def import djangoImportSetup
djangoImportSetup()
from CCapp.models import *
from CCapp.defs import makeDirFile,makeImportPath,logconfig,logException,logsOutput,readFile,executeFunction
from django.db import transaction
import random
from itertools import cycle
import csv
import json
import random

USER_CSV_PATH = "user.csv"
OUTPUT_JSON_PATH = "offers.json"

def load_users_from_csv(file_path):
    users = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("authority") == "2":
                users.append(row.get("mail"))
    return users

def generate_offers(num_offers, users):
    offers = []
    for i in range(1, num_offers + 1):
        offer_name = f"求人{i:06d}"
        num_users = random.randint(1, 10)
        selected_users = random.sample(users, num_users)
        offers.append({
            "offerName": offer_name,
            "users": [{"mail": mail} for mail in selected_users]
        })
    return offers

def main():
    users = load_users_from_csv(USER_CSV_PATH)
    if not users:
        print("エラー: authorityが2のユーザーが見つかりませんでした。")
        return

    num_offers = 400000
    offers = generate_offers(num_offers, users)

    with open(OUTPUT_JSON_PATH, mode='w', encoding='utf-8') as file:
        json.dump(offers, file, ensure_ascii=False, indent=2)
    print(f"{num_offers}件の求人データを {OUTPUT_JSON_PATH} に保存しました。")

if __name__ == "__main__":
    main()

