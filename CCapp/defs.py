import os
import sys
import time
import json
import csv
import logging
import django

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