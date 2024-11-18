import os
import time
import json
import csv
import logging

def makeDirFile(dir,file):
    if not os.path.exists(dir):
        os.makedirs(dir)
    if not os.path.exists(file):
        with open(file,'w',encoding='utf-8') as f:
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
    """例外をログに記録する"""
    logger.error(f"{file_key}: エラーが発生しました - {exception}")

def logsPrints(*args,**kwargs):
    logging.info(*args,**kwargs)
    prints(*args,**kwargs)

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
    print(f'実行時間: {elapsedTime:.4f} 秒')

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