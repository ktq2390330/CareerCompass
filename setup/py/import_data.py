import os
import logging
import datetime
from django_setup_def import djangoImportSetup
djangoImportSetup()
from CCapp.models import *
from CCapp.defs import makeDirFile,makeImportPath,logconfig,logException,logsOutput,readFile,executeFunction
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

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
        if created:
            results.append(f"新規作成: {instance.name}")
        else:
            results.append(f"既存データ取得: {instance.name}")
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
            logException(logger,file_key,FileNotFoundError)
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            logException(logger,file_key,e)
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
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for row in data:
                    mail,furigana,nationality,birth,gender,graduation,school,sClass,sol,departments,tel,address,category00name,category01name,category10name,category11name,area1name,uOffer=row
                    ['mail'],row['furigana'],row['nationality'],row['birth'].split('-'),row['gender'],row['graduation'],row['school'],row['class'],row['sol'],row['departments'],row['tel'],row['address'],row
                    ['category00name'],row['category01name'],row['category10name'],row['category11name'],row['area1name'],row['uOffer']
                    birth=datetime.date(birth)
                    user=User.objects.get(mail=mail)
                    area1=Area1.objects.get(name=area1name)
                    category00=Category00.objects.get(name=category00name)
                    category01=Category01.objects.get(name=category01name)
                    category10=Category10.objects.get(name=category10name)
                    category11=Category11.objects.get(name=category11name)
                    instance,created=Profile.objects.get_or_create(user=user,furigana=furigana,nationality=nationality,birth=birth,gender=gender,graduation=graduation,uSchool=school,sClass=sClass,sol=sol,
                    departments=departments,uTel=tel,uAddress=address,category00=category00,category01=category01,category10=category10,category11=category11,area1=area1,uOffer=uOffer)
                    instanceDict[instance]=created
        except User.DoesNotExist:
            print(f"mail: {mail} は存在しません")
        except Area1.DoesNotExist:
            print(f'area1: {area1name} は存在しません')
        except Category00.DoesNotExist:
            print(f"category00: {category00name} は存在しません")
        except Category01.DoesNotExist:
            print(f"category01: {category01name} は存在しません")
        except Category10.DoesNotExist:
            print(f"category10: {category10name} は存在しません")
        except Category10.DoesNotExist:
            print(f"category11: {category11name} は存在しません")
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
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

def offer(filePath):
    instanceDict = {}
    def function():
        try:
            data = readFile(filePath)
            with transaction.atomic():
                for row_num, row in enumerate(data, start=1):  # 行番号を追跡
                    try:
                        # 辞書形式から必要なデータを取得
                        title = row['title']
                        detail = row['detail']
                        solicitation = row['solicitation']
                        course = row['course']
                        forms = row['forms']
                        roles = row['roles']
                        CoB = row['CoB']
                        subject = row['subject']
                        NoP = row['NoP']
                        departments = row['departments']
                        characteristic = row['characteristic']
                        pes = row['PES']
                        giving = row['giving']
                        allowances = row['allowances']
                        salaryRaise = row['salaryRaise']
                        bonus = row['bonus']
                        holiday = row['holiday']
                        workingHours = row['workingHours']
                        area1name = row['area1name']
                        category00name = row['category00name']
                        category01name = row['category01name']
                        category10name = row['category10name']
                        category11name = row['category11name']
                        corporationId = row['corporationID']
                        period_str = row['period']
                        status_str = row['status']

                        # 関連オブジェクトの取得
                        print(f"検索値 - area1name: {area1name}, category00name: {category00name}, category01name: {category01name}, category10name: {category10name}, category11name: {category11name}, corporationId: {corporationId}")
                        area1 = Area1.objects.get(name=area1name)
                        category00 = Category00.objects.get(name=category00name)
                        category01 = Category01.objects.get(name=category01name)
                        category10 = Category10.objects.get(name=category10name)
                        category11 = Category11.objects.get(name=category11name)
                        corporation = Corporation.objects.get(corp=corporationId)
                    except KeyError as e:
                        print(f"キーエラー: {e}, 行番号={row_num}, 行データ: {row}")
                        continue
                    except Area1.DoesNotExist:
                        print(f"Area1オブジェクトが見つかりません: name={area1name}, 該当データ: {row}")
                        continue
                    except Category00.DoesNotExist:
                        print(f"Category00オブジェクトが見つかりません: name={category00name}, 該当データ: {row}")
                        continue
                    except Category01.DoesNotExist:
                        print(f"Category01オブジェクトが見つかりません: name={category01name}, 該当データ: {row}")
                        continue
                    except Category10.DoesNotExist:
                        print(f"Category10オブジェクトが見つかりません: name={category10name}, 該当データ: {row}")
                        continue
                    except Category11.DoesNotExist:
                        print(f"Category11オブジェクトが見つかりません: name={category11name}, 該当データ: {row}")
                        continue
                    except Corporation.DoesNotExist:
                        print(f"Corporationオブジェクトが見つかりません: corp={corporationId}, 該当データ: {row}")
                        continue

                    try:
                        # 日付のパース
                        period = datetime.datetime.strptime(period_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError as e:
                        print(f"日付形式エラー: {e}, 行番号={row_num}, 日付文字列: {period_str}")
                        continue

                    # ステータスのパース
                    status = status_str.lower() == 'true'

                    # Offerインスタンス作成
                    instance, created = Offer.objects.get_or_create(
                        name=title, detail=detail, solicitation=solicitation, course=course,
                        forms=forms, roles=roles, CoB=CoB, subject=subject, NoP=NoP,
                        departments=departments, characteristic=characteristic, PES=pes, giving=giving,
                        allowances=allowances, salaryRaise=salaryRaise, bonus=bonus, holiday=holiday,
                        workingHours=workingHours, area1=area1, category00=category00,
                        category01=category01, category10=category10, category11=category11,
                        corporation=corporation, period=period, status=status
                    )
                    instanceDict[instance] = created

        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")

    executeFunction(function)
    outputQueryResults(instanceDict)


def offerEntry(filePath):
    instanceDict={}
    def function():
        try:
            data=readFile(filePath)
            with transaction.atomic():
                for offerData in data:
                    offerId=offerData['offerId']
                    offer=Offer.objects.get(id=offerId)
                    for userData in offerData['users']:
                        userId=userData['userId']
                        user=User.objects.get(id=userId)
                        _,created=OfferEntry.objects.get_or_create(offer=offer,user=user)
                        instanceDict[(offer.id,user.id)]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Offer.DoesNotExist:
            print(f"offerID: {offerId} は存在しません")
        except User.DoesNotExist:
            print(f"userID: {userId} は存在しません")
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
                    offerId=offerData['offerId']
                    offer=Offer.objects.get(id=offerId)
                    for tagData in offerData['tags']:
                        name=tagData['name']
                        tag=Tag.objects.get(name=name)
                        _,created=offer.welfare.get_or_create(tag)
                        instanceDict[(offer.id,tag.name)]=created
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {filePath}")
        except Offer.DoesNotExist:
            print(f"offerID: {offerId} は存在しません")
        except Tag.DoesNotExist:
            print(f"tagName: {name} は存在しません")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    executeFunction(function)
    outputQueryResults(instanceDict)

# 実行
functionMap={
    # 'area0.csv':area0,
    # 'area1.csv':area1,
    # 'area2.csv':area2,
    # 'category00.csv':category00,
    # 'category01.csv':category01,
    # 'category10.csv':category10,
    # 'category11.csv':category11,
    # 'tag.csv':tag,
    # 'user.csv':user,
    # 'profile.csv':profile,
    # 'question00.csv':question00,
    # 'question01.csv':question01,
    # 'assessment.csv':assessment,
    # 'corporation.csv':corporation,
    # 'DM.csv':dm,
    # 'offer.csv':offer,
    # 'offerEntry.json':offerEntry,
    'offerTag': offerTag,
    # 'supportDM.csv':supportDM,
}
logger=import_data_SettingLogs()

for file_key,function in functionMap.items():
    basePath='../setup/data/'
    file_path=makeImportPath(basePath,file_key)
    logger.info(f"Loading data for {file_key} from {file_path}...")
    function(file_path)

logging.info('Executed all.')