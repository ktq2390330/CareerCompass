import time
import json
import csv

def prints(*args,**kwargs):
    print('\n------------------------------------------------\n')
    print(*args,**kwargs)

def measureExecutionTime(function,*args,**kwargs):
	startTime=time.time()
	result=function(*args,**kwargs)
	endTime=time.time()
	return endTime-startTime,result

def displayExecutionResults(function,filePath):
    elapsedTime,_=measureExecutionTime(function,filePath)
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