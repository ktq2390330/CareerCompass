import os
import time
import json
import csv
import logging

def makeDirFile(file_name):
    file_path=os.path.join(file_name)
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path,'w',encoding='utf-8') as f:
            pass
    return logging.getLogger(__name__)

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

#ファイルの内容を読み取る関数（CSVまたはJSON対応）
def readFile(filePath):
    if filePath.endswith('.csv'):
        with open(filePath,newline='',encoding='utf-8') as file:
            if filePath.find('.csv')!=-1:
                return list(csv.DictReader(file))
    elif filePath.endswith('.json'):
        with open(filePath,'r',encoding='utf-8') as file:
            return json.load(file)
    else:
        raise ValueError("サポートされていないファイル形式です。CSVまたはJSONファイルを使用してください。")