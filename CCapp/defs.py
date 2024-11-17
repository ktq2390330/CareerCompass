import time
import json
import csv

def prints(*args,**kwargs):
    print('\n------------------------------------------------\n')
    print(*args,**kwargs)

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