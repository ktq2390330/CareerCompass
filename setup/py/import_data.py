import os
import logging
import datetime
from django_setup_def import djangoImportSetup
djangoImportSetup()
from CCapp.models import *
from CCapp.defs import *
from django.db import transaction
from datetime import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# ログの設定
def import_data_SettingLogs():
    logDir=os.path.join('logs')
    logFile=os.path.join(f'{logDir}/data_import.log')
    logconfig(logFile)
    logger=makeDirFile(logFile)
    return logger

#インスタンスの作成または取得結果
def queryResults(instanceDict):
    results=['処理結果\n']
    for instance,created in instanceDict.items():
        instance_name = getattr(instance, 'name', str(instance))
        if created:
            results.append(f"新規作成: {instance_name}")
        else:
            results.append(f"既存データ取得: {instance_name}")
    return results

def outputQueryResults(instanceDict):
    results=queryResults(instanceDict)
    logsOutput(*results)

def area0(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    regionName=row['name']
                    instance,created=Area0.objects.get_or_create(name=regionName)
                    instanceDict[instance]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def area1(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    regionName,prefecture=row['region'], row['name']
                    region=Area0.objects.get(name=regionName)
                    instance,created=Area1.objects.get_or_create(name=prefecture,area0=region)
                    instanceDict[instance]=created
        except Area0.DoesNotExist:
            print(f"area0: {region} は存在しません")
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def area2(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    prefecture_name,city_name=row['都道府県名（漢字）'],row['市区町村名（漢字）']
                    prefecture=Area1.objects.get(name=prefecture_name)
                    instance,created=Area2.objects.get_or_create(name=city_name,area1=prefecture)
                    instanceDict[instance]=created
        except Area1.DoesNotExist:
            print(f"area1: {prefecture_name} は存在しません")
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def tag(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    tagName=row['name']
                    instance,created=Tag.objects.get_or_create(name=tagName)
                    instanceDict[instance]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def category00(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    categoryName=row['name']
                    instance,created=Category00.objects.get_or_create(name=categoryName)
                    instanceDict[instance]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def category01(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    category00Name, category01Name = row['category00name'], row['name']
                    category00= Category00.objects.get(name=category00Name)
                    instance,created=Category01.objects.get_or_create(name=category01Name,category00=category00)
                    instanceDict[instance]=created
        except Category00.DoesNotExist:
            print(f"category00: {category00Name} は存在しません")
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def category10(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    categoryName = row['name']
                    instance,created=Category10.objects.get_or_create(name=categoryName)
                    instanceDict[instance]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def category11(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    category10Name, category11Name = row['category10name'], row['name']
                    category10=Category10.objects.get(name=category10Name)
                    instance,created=Category11.objects.get_or_create(name=category11Name,category10=category10)
                    instanceDict[instance]=created
        except Category10.DoesNotExist:
            print(f"{category10Name} は存在しません")
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def user(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    name,mail,password,authority=row['name'],row['mail'],row['password'],row['authority']
                    instance,created=User.objects.get_or_create(name=name,mail=mail,password=password,authority=authority)
                    instanceDict[instance]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def profile(filePath):
    instanceDict = {}

    def clean_data(data):
        required_columns = {'mail', 'furigana', 'birth', 'gender', 'graduation', 'school', 'tel', 'address'}
        cleaned_data = []

        # ファイルに存在するカラムをチェック
        actual_columns = data[0].keys() if data else []
        if not all(col in actual_columns for col in required_columns):
            missing_columns = [col for col in required_columns if col not in actual_columns]
            print(f"ファイルに必要なカラムが存在しません: {missing_columns}")
            print(f"ファイル内のカラム: {list(actual_columns)}")  # 現在のカラム一覧を出力
            return []

        for row in data:
            # 必要なカラムのみ抽出
            filtered_row = {key: row.get(key) for key in required_columns}

            # 必須カラムの欠損チェック
            missing_values = [key for key in required_columns if not filtered_row.get(key)]
            if missing_values:
                print(f"以下のカラムが不足しています: {missing_values}")
                continue

            # データ型の検証と変換
            try:
                filtered_row['birth'] = datetime.strptime(filtered_row['birth'], '%Y/%m/%d').date()
            except ValueError:
                print(f"無効な日付形式: {filtered_row['birth']}")
                continue

            cleaned_data.append(filtered_row)

        return cleaned_data

    def function():
        try:
            # ファイルを読み込む
            data = readFile(filePath)
            if not data or not isinstance(data, list):
                print("データが空または無効です。処理を終了します。")
                return

            # データをクリーニング
            data = clean_data(data)
            if not data:
                print("有効なデータが存在しません。")
                return

            with transaction.atomic():
                for row in data:
                    try:
                        user = User.objects.get(mail=row['mail'])
                        instance, created = Profile.objects.get_or_create(
                            user=user,
                            furigana=row['furigana'],
                            birth=row['birth'],
                            gender=row['gender'],
                            graduation=row['graduation'],
                            uSchool=row['school'],
                            uTel=row['tel'],
                            uAddress=row['address']
                        )
                        instanceDict[instance] = created

                    except User.DoesNotExist:
                        print(f"mail: {row['mail']} は存在しません")
                    except KeyError as key_error:
                        print(f"データが不正です。キーが見つかりません: {key_error}")

        except Exception as e:
            print(f"エラーが発生しました: {e}")

    executeFunction(function)
    outputQueryResults(instanceDict)

def question00(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    questionName=row['name']
                    instance,created=Question00.objects.get_or_create(name=questionName)
                    instanceDict[instance]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def question01(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    question00Name,name=row['question00name'], row['name']
                    question00=Question00.objects.get(name=question00Name)
                    instance,created=Question01.objects.get_or_create(name=name,question00=question00)
                    instanceDict[instance]=created
        except Category10.DoesNotExist:
            print(f"{question00Name} は存在しません")
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def assessment(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    mail,question01Name,answer=row['mail'],row['question01name'],row['answer']
                    user=User.objects.get(mail=mail)
                    question01=Question01.objects.get(question01Name)
                    instance,created=User.objects.get_or_create(user=user,question01=question01,answer=answer)
                    instanceDict[instance]=created
        except User.DoesNotExist:
            print(f"mail: {mail} は存在しません")
        except Question01.DoesNotExist:
            print(f"questionName: {question01Name} は存在しません")
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def corporation(filePath):
    instanceDict = {}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    required_keys=['cId','name','address','mail','tel','url']
                    if not all(key in row for key in required_keys):
                        print(f"不足しているデータ: {row}")
                        continue
                    try:
                        cId,name,address,mail,tel,url=(row['cId'],row['name'],row['address'],row['mail'],row['tel'],row['url'])
                    except ValueError as ve:
                        print(f"データ変換エラー: {ve}, 行: {row}")
                        continue
                    instance,created=Corporation.objects.get_or_create(corp=cId,name=name,address=address,cMail=mail,cTel=tel,url=url)
                    instanceDict[instance]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)


def dm(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    title,detail,read,userId,corpId=row['title'],row['detail'],row['read'],row['userID'],row['corporationID']
                    user=User.objects.get(id=userId)
                    corp=Corporation.objects.get(id=corpId)
                    instance,created=Corporation.objects.get_or_create(name=title,detail=detail,read=read,user=user,corp=corp)
                    instanceDict[instance]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except User.DoesNotExist:
            print(f"userID: {userId} は存在しません")
        except Corporation.DoesNotExist:
            print(f'法人番号: {corpId} は存在しません')
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def supportDM(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    title,detail,read,userSendId,userReceiveId=row['title'],row['detail'],row['read'],row['sendUserID'],row['receiveUserID']
                    userSend,userReceive=User.objects.get(id=userSendId),User.objects.get(id=userReceiveId)
                    instance,created=Corporation.objects.get_or_create(name=title,detail=detail,read=read,userSend=userSend,userReceive=userReceive)
                    instanceDict[instance]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except User.DoesNotExist:
                print(f"userID: {userSend} または、userID: {userReceive} は存在しません")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

#!更新対応Ver
# def offer(filePath):
#     def process_data(data):
#         # 既存データを一括取得してキャッシュ
#         existing_offers = {o.name: o for o in Offer.objects.all()}  # 'name' をユニークキーと仮定
#         rows_to_insert = []
#         rows_to_update = []
#         errors = []

#         for row_num, row in enumerate(tqdm(data, desc="Processing Rows", unit="row"), start=1):
#             try:
#                 required_keys = ['title', 'detail', 'solicitation', 'course', 'forms', 'roles',
#                                 'CoB', 'subject', 'NoP', 'departments', 'characteristic', 'PES',
#                                 'giving', 'allowances', 'salaryRaise', 'bonus', 'holiday',
#                                 'workingHours', 'area1name', 'category00name', 'category01name',
#                                 'category10name', 'category11name', 'corporationID', 'period', 'status']

#                 if not all(key in row for key in required_keys):
#                     raise KeyError(f"欠損キー: {set(required_keys) - row.keys()}")

#                 area1 = Area1.objects.get(name=row['area1name'])
#                 category00 = Category00.objects.get(name=row['category00name'])
#                 category01 = Category01.objects.get(name=row['category01name'])
#                 category10 = Category10.objects.get(name=row['category10name'])
#                 category11 = Category11.objects.get(name=row['category11name'])
#                 corporation = Corporation.objects.get(corp=row['corporationID'])

#                 period = datetime.strptime(row['period'], "%Y-%m-%d %H:%M:%S")
#                 status = row['status'].lower() == 'true'

#                 # 挿入または更新の判断
#                 if row['title'] in existing_offers:
#                     # 既存レコードのインスタンスを取得して更新
#                     existing_offer = existing_offers[row['title']]
#                     existing_offer.detail = row['detail']
#                     existing_offer.solicitation = row['solicitation']
#                     existing_offer.course = row['course']
#                     existing_offer.forms = row['forms']
#                     existing_offer.roles = row['roles']
#                     existing_offer.CoB = row['CoB']
#                     existing_offer.subject = row['subject']
#                     existing_offer.NoP = row['NoP']
#                     existing_offer.departments = row['departments']
#                     existing_offer.characteristic = row['characteristic']
#                     existing_offer.PES = row['PES']
#                     existing_offer.giving = row['giving']
#                     existing_offer.allowances = row['allowances']
#                     existing_offer.salaryRaise = row['salaryRaise']
#                     existing_offer.bonus = row['bonus']
#                     existing_offer.holiday = row['holiday']
#                     existing_offer.workingHours = row['workingHours']
#                     existing_offer.area1 = area1
#                     existing_offer.category00 = category00
#                     existing_offer.category01 = category01
#                     existing_offer.category10 = category10
#                     existing_offer.category11 = category11
#                     existing_offer.corporation = corporation
#                     existing_offer.period = period
#                     existing_offer.status = status
#                     rows_to_update.append(existing_offer)
#                 else:
#                     # 新規挿入
#                     rows_to_insert.append(Offer(
#                         name=row['title'], detail=row['detail'], solicitation=row['solicitation'], course=row['course'],
#                         forms=row['forms'], roles=row['roles'], CoB=row['CoB'], subject=row['subject'], NoP=row['NoP'],
#                         departments=row['departments'], characteristic=row['characteristic'], PES=row['PES'],
#                         giving=row['giving'], allowances=row['allowances'], salaryRaise=row['salaryRaise'],
#                         bonus=row['bonus'], holiday=row['holiday'], workingHours=row['workingHours'], area1=area1,
#                         category00=category00, category01=category01, category10=category10, category11=category11,
#                         corporation=corporation, period=period, status=status
#                     ))

#             except Exception as e:
#                 errors.append((row_num, str(e)))

#         return rows_to_insert, rows_to_update, errors

#     def function():
#         try:
#             data = readFile(filePath)
#             rows_to_insert, rows_to_update, errors = process_data(data)

#             with transaction.atomic():
#                 # 新規挿入
#                 Offer.objects.bulk_create(rows_to_insert, batch_size=1000, ignore_conflicts=True)

#                 # 更新処理
#                 if rows_to_update:
#                     Offer.objects.bulk_update(
#                         rows_to_update,
#                         fields=[
#                             'detail', 'solicitation', 'course', 'forms', 'roles', 'CoB', 'subject', 'NoP',
#                             'departments', 'characteristic', 'PES', 'giving', 'allowances', 'salaryRaise',
#                             'bonus', 'holiday', 'workingHours', 'area1', 'category00', 'category01', 'category10',
#                             'category11', 'corporation', 'period', 'status'
#                         ],
#                         batch_size=1000
#                     )

#             # 処理結果の出力
#             print(f"新規挿入: {len(rows_to_insert)}件")
#             print(f"更新: {len(rows_to_update)}件")
#             if errors:
#                 print(f"エラーが発生しました ({len(errors)}件):")
#                 for row_num, error_msg in errors[:10]:
#                     print(f"行 {row_num}: {error_msg}")
#                 if len(errors) > 10:
#                     print("...他にもエラーがあります")

#         except FileNotFoundError:
#             print(f"ファイルが見つかりません: {filePath}")
#         except Exception as e:
#             print(f"予期せぬエラーが発生しました: {e}")

#     executeFunction(function)


#!パフォーマンス優先
def offer(filePath):
    def process_data(data):
        # 事前キャッシュ
        area1_cache = {a.name: a for a in Area1.objects.all()}
        category00_cache = {c.name: c for c in Category00.objects.all()}
        category01_cache = {c.name: c for c in Category01.objects.all()}
        category10_cache = {c.name: c for c in Category10.objects.all()}
        category11_cache = {c.name: c for c in Category11.objects.all()}
        corporation_cache = {c.corp: c for c in Corporation.objects.all()}

        rows_to_insert = []
        errors = []  # エラーを記録するリスト
        success_count = 0

        for row_num, row in enumerate(tqdm(data, desc="Processing Rows", unit="row"), start=1):
            try:
                # 必要なデータの取得と検証
                required_keys = ['title', 'detail', 'solicitation', 'course', 'forms', 'roles',
                                'CoB', 'subject', 'NoP', 'departments', 'characteristic', 'PES',
                                'giving', 'allowances', 'salaryRaise', 'bonus', 'holiday',
                                'workingHours', 'area1name', 'category00name', 'category01name',
                                'category10name', 'category11name', 'corporationID', 'period', 'status']

                if not all(key in row for key in required_keys):
                    raise KeyError(f"欠損キー: {set(required_keys) - row.keys()}")

                area1 = area1_cache.get(row['area1name'])
                category00 = category00_cache.get(row['category00name'])
                category01 = category01_cache.get(row['category01name'])
                category10 = category10_cache.get(row['category10name'])
                category11 = category11_cache.get(row['category11name'])
                corporation = corporation_cache.get(row['corporationID'])

                if not all([area1, category00, category01, category10, category11, corporation]):
                    raise ValueError(f"関連オブジェクトが見つかりません: {row}")

                period = datetime.strptime(row['period'], "%Y-%m-%d %H:%M:%S")
                status = row['status'].lower() == 'true'

                rows_to_insert.append(Offer(
                    name=row['title'], detail=row['detail'], solicitation=row['solicitation'], course=row['course'],
                    forms=row['forms'], roles=row['roles'], CoB=row['CoB'], subject=row['subject'], NoP=row['NoP'],
                    departments=row['departments'], characteristic=row['characteristic'], PES=row['PES'],
                    giving=row['giving'], allowances=row['allowances'], salaryRaise=row['salaryRaise'],
                    bonus=row['bonus'], holiday=row['holiday'], workingHours=row['workingHours'], area1=area1,
                    category00=category00, category01=category01, category10=category10, category11=category11,
                    corporation=corporation, period=period, status=status
                ))

            except Exception as e:
                errors.append((row_num, str(e)))  # エラー情報を記録

        return rows_to_insert, errors, success_count

    def function():
        try:
            data = readFile(filePath)
            rows_to_insert, errors, success_count = process_data(data)

            with transaction.atomic():
                created_instances = Offer.objects.bulk_create(rows_to_insert, batch_size=1000)
                success_count = len(created_instances)  # 成功したレコード数を記録

            # 処理結果を出力
            print(f"処理完了: {success_count}件のレコードが成功しました")
            if errors:
                print(f"エラーが発生しました ({len(errors)}件):")
                for row_num, error_msg in errors[:10]:  # 最初の10件のみ表示
                    print(f"行 {row_num}: {error_msg}")
                if len(errors) > 10:
                    print("...他にもエラーがあります")

        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")

    executeFunction(function)

def offerEntry(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for offerData in data:
                    name=offerData['offerName']
                    offer=Offer.objects.get(name=name)
                    for userData in offerData['users']:
                        mail=userData['mail']
                        user=User.objects.get(mail=mail)
                        _,created=OfferEntry.objects.get_or_create(offer=offer,user=user)
                        instanceDict[(offer.name,user.mail)]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Offer.DoesNotExist:
            print(f"offerName: {name} は存在しません")
        except User.DoesNotExist:
            print(f"mail: {mail} は存在しません")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

def offerTag(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for offerData in data:
                    offerName=offerData['offerName']
                    offer=Offer.objects.get(name=offerName)
                    for tagData in offerData['tags']:
                        name=tagData['name']
                        tag=Tag.objects.get(name=name)
                        _,created=Offer.welfare.through.objects.get_or_create(tag=tag,offer=offer)
                        instanceDict[(offer.name,tag.name)]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Offer.DoesNotExist:
            print(f"offerName: {offerName} は存在しません")
        except Tag.DoesNotExist:
            print(f"tagName: {name} は存在しません")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

# 実行
logger = import_data_SettingLogs()

def process_file(file_key, function, base_path):
    try:
        file_path = makeImportPath(base_path, file_key)
        logger.info(f"Processing started: {file_key} -> {file_path}")
        function(file_path)
        logger.info(f"Processing completed: {file_key}")
    except Exception as e:
        logger.error(f"Error while processing {file_key}: {e}")

def process_multiple_files(base_path, file_prefix, function, count):
    for i in range(1, count + 1):
        file_key = f"{file_prefix}{i}.csv"
        process_file(file_key, function, base_path)

def main():
    function_map = {
        'area0.csv': area0,
        'area1.csv': area1,
        'area2.csv': area2,
        'category00.csv': category00,
        'category01.csv': category01,
        'category10.csv': category10,
        'category11.csv': category11,
        'tag.csv': tag,
        'user.csv': user,
        'profile.csv': profile,
        'question00.csv': question00,
        'question01.csv': question01,
        'assessment.csv': assessment,
        'corporation.csv': corporation,
        'offer': (offer, 4),
        'offerEntry.json': offerEntry,
        'offerTag.json': offerTag,
    }

    base_path = '../setup/data/'

    for key, value in function_map.items():
        if isinstance(value, tuple):
            function, file_count = value
            logger.info(f"Starting processing for {key} with {file_count} files.")
            process_multiple_files(base_path, key, function, file_count)
        else:
            logger.info(f"Starting file processing: {key}")
            process_file(key, value, base_path)

    logger.info("All processing tasks have been completed.")

if __name__ == "__main__":
    main()