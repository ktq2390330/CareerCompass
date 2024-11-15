import os
import sys
import django
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), "/CareerCompass")) #Cドライブ直下の場合
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CareerCompassProject.settings')
django.setup()
from CCapp.models import *
from django.db import transaction

def makePath(fileName):
    csvFilePath='/CareerCompass/setup/csv/'
    filePath=os.path.join(os.path.dirname(__file__),f'{csvFilePath}{fileName}.csv')
    return filePath

def returnPrint(instanceDict):
    for instance,created in instanceDict.items():
        if created==None:
            print(f"作成されたデータ: {instance.name}")
        elif created:
            print(f"新規作成: {instance.name}")
        else:
            print(f"既存データ取得: {instance.name}")

def area0(filePath):
    instanceDict={}
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            with transaction.atomic():
                for row in reader:
                    regionName = row['name']
                    instance,created=Area0.objects.get_or_create(name=regionName)
                    instanceDict[instance]=created
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    returnPrint(instanceDict)

def area1(filePath):
    instanceDict={}
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            next(reader)
            with transaction.atomic():
                for row in reader:
                    regionName,prefecture = row['region'], row['name']
                    region = Area0.objects.get(name=regionName)
                    instance=Area1.objects.create(name=prefecture, area0=region)
                    instanceDict[instance]=''
    except Area0.DoesNotExist:
        print(f"{region} は存在しません")
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    returnPrint(instanceDict)

def area2(filePath):
    instanceDict={}
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            next(reader)
            with transaction.atomic():
                for row in reader:
                    prefecture_name, city_name = row['都道府県名（漢字）'], row['市区町村名（漢字）']
                    prefecture= Area1.objects.get(name=prefecture_name)
                    instance=Area2.objects.create(name=city_name, area1=prefecture)
                    instanceDict[instance]=None
    except Area1.DoesNotExist:
        print(f"{prefecture_name} は存在しません")
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    returnPrint(instanceDict)

def tag(filePath):
    instanceDict={}
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            with transaction.atomic():
                for row in reader:
                    tagName = row['name']
                    instance,created=Tag.objects.get_or_create(name=tagName)
                    instanceDict[instance]=created
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    returnPrint(instanceDict)

def category00(filePath):
    instanceDict={}
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            with transaction.atomic():
                for row in reader:
                    categoryName = row['name']
                    instance,created=Category00.objects.get_or_create(name=categoryName)
                    instanceDict[instance]=created
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    returnPrint(instanceDict)

def category01(filePath):
    instanceDict={}
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            next(reader)
            with transaction.atomic():
                for row in reader:
                    category00Name, category01Name = row['category00name'], row['name']
                    category00= Category00.objects.get(name=category00Name)
                    instance=Category01.objects.create(name=category01Name, category00=category00)
                    instanceDict[instance]=None
    except Category00.DoesNotExist:
        print(f"{category00Name} は存在しません")
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    returnPrint(instanceDict)

def category10(filePath):
    instanceDict={}
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            with transaction.atomic():
                for row in reader:
                    categoryName = row['name']
                    instance,created=Category10.objects.get_or_create(name=categoryName)
                    instanceDict[instance]=created
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    returnPrint(instanceDict)

def category11(filePath):
    instanceDict={}
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            next(reader)
            with transaction.atomic():
                for row in reader:
                    category10Name, category11Name = row['category10name'], row['name']
                    category10 = Category10.objects.get(name=category10Name)
                    instance=Category11.objects.create(name=category11Name, category10=category10)
                    instanceDict[instance]=None
    except Category10.DoesNotExist:
        print(f"{category10Name} は存在しません")
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    returnPrint(instanceDict)

def corporation(filePath):
    instanceDict={}
    try:
        with open(filePath, newline='', encoding='utf-8') as csvFile:
            reader = csv.DictReader(csvFile)
            with transaction.atomic():
                for row in reader:
                    cId,name,address,mail,tel,url=row['cId'],row['name'],row['address'],row['tel'],row['url']
                    instance,created=Corporation.objects.get_or_create(corp=cId,cName=name,address=address,cMail=mail,cTel=tel,url=url)
                    instanceDict[instance]=created
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filePath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    returnPrint(instanceDict)

# def dm(filePath):
#     instanceDict={}
#     try:
#         with open(filePath, newline='', encoding='utf-8') as csvFile:
#             reader = csv.DictReader(csvFile)
#             with transaction.atomic():
#                 for row in reader:
#                     title,detail,read,userId,tel,url=row['title'],row['detail'],row['read'],row['userID'],row['corporationID']
#                     instance,created=Corporation.objects.get_or_create(corp=cId,cName=name,address=address,cMail=mail,cTel=tel,url=url)
#                     instanceDict[instance]=created
#     except FileNotFoundError:
#         print(f"ファイルが見つかりません: {filePath}")
#     except Exception as e:
#         print(f"エラーが発生しました: {e}")
#     returnPrint(instanceDict)



# 実行
functionMap={
    'area0':area0,
    'area1':area1,
    'area2':area2,
    'category00':category00,
    'category01':category01,
    'category10':category10,
    'category11':category11,
    # 'corporation':corporation,
    # 'DM':dm,
    # 'offer':offer,
    # 'profile':profile,
    # 'supportDM':supportDM,
    'tag':tag,
    # 'user':user,
}

for file_key, function in functionMap.items():
    file_path = makePath(file_key)
    print(f"Loading data for {file_key} from {file_path}...")
    function(file_path)