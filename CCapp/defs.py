import os
import sys
import time
import json
import csv
import logging
import django
import codecs
import chardet

#Djangoプロジェクトの設定
def djangoSetup():
	project_root=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
	sys.path.append(project_root)
	os.environ.setdefault('DJANGO_SETTINGS_MODULE','CareerCompassProject.settings')
	django.setup()

def makeDirFile(file_name):
    file_path=os.path.join(file_name)
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path,'w',encoding='utf-8') as f:
            pass
    return logging.getLogger(__name__)

#ファイルパス生成関数
def makeImportPath(basePath,fileName):
    filePath=os.path.join(os.path.dirname(__file__),f'{basePath}{fileName}')
    return filePath

def prints(*args,**kwargs):
    print('\n------------------------------------------------\n')
    print(*args,**kwargs)

def logconfig(log_file):
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file,mode='a',encoding='utf-8'),
        logging.StreamHandler()
        ]
    )

def logException(logger,file_key,exception):
    logger.error(f"{file_key}: エラーが発生しました - {exception}")

def logsOutput(*args,**kwargs):
    message="\n".join(str(arg) for arg in args)
    logging.info(message,**kwargs)

def measureExecutionTime(function,*args,**kwargs):
    start_time=time.time()
    if args or kwargs:
        result=function(*args, **kwargs)
    else:
        result=function()
    elapsed_time=time.time()-start_time
    return elapsed_time,result

def executeFunction(function,*args,**kwargs):
    elapsedTime,_=measureExecutionTime(function,*args,**kwargs)
    logging.info(f'実行時間: {elapsedTime:.4f} 秒')

#ファイルの内容を読み取る関数（対応ファイル:csv,json,txt）
def readFile(filePath):
    logsOutput(filePath)
    try:
        if filePath.endswith('.csv'):
            with open(filePath,newline='',encoding='utf-8') as file:
                if filePath.find('.csv')!=-1:
                    return list(csv.DictReader(file))
        elif filePath.endswith('.json'):
            with open(filePath,'r',encoding='utf-8') as file:
                return json.load(file)
        elif filePath.endswith('.txt'):
            with open(filePath,'r',encoding='utf-8') as file:
                return file.read()
        else:
            raise ValueError("サポートされていないファイル形式です。TEXT,CSVまたはJSONファイルを使用してください。")
    except Exception as e:
        print(f'error in readFile: {e}')
        return None

# ファイルへの書き込み関数（対応ファイル: csv, json, txt）
def writeFile(filePath, data):
    logsOutput(filePath)
    try:
        if filePath.endswith('.csv'):
            with open(filePath, mode='w', newline='', encoding='utf-8') as file:
                if isinstance(data, list) and data:
                    writer = csv.DictWriter(file, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    raise ValueError("CSV書き込みにはリスト形式のデータが必要です。")
        elif filePath.endswith('.json'):
            with open(filePath, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        elif filePath.endswith('.txt'):
            with open(filePath, 'w', encoding='utf-8') as file:
                file.write(data)
        else:
            raise ValueError("サポートされていないファイル形式です。TEXT, CSVまたはJSONファイルを使用してください。")
    except Exception as e:
        print(f'error in writeFile: {e}')
        return False
    return True

def detect_encoding(file_path):
    """
    ファイルのエンコーディングを検出します。

    Parameters:
        file_path (str): 検出するファイルのパス

    Returns:
        str: 検出されたエンコーディング
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def convert_to_utf8_with_detection(input_file, output_file):
    """
    ファイルのエンコーディングを自動検出してUTF-8に変換します。

    Parameters:
        input_file (str): 入力ファイルのパス
        output_file (str): 変換後の出力ファイルのパス
    """
    try:
        # ファイルのエンコーディングを検出
        detected_encoding = detect_encoding(input_file)
        print(f"検出されたエンコーディング: {detected_encoding}")

        # 入力ファイルを検出されたエンコーディングで読み込む
        with codecs.open(input_file, 'r', encoding=detected_encoding) as infile:
            content = infile.read()

        # UTF-8 エンコードで出力ファイルに書き込む
        with codecs.open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(content)

        print(f"変換が完了しました: {output_file}")

    except Exception as e:
        print(f"エンコード変換中にエラーが発生しました: {e}")
