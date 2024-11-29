import csv
from django_setup_def import djangoImportSetup
djangoImportSetup()
from CCapp.models import *
from CCapp.defs import readFile,writeFile,makeImportPath

# CSVファイルにデータを書き込む
filename = 'offer.csv'

# CSVのヘッダー
headers = [
    "name", "detail", "solicitation", "course", "forms", "roles", "CoB", 
    "subject", "NoP", "departments", "characteristic", "PES", "giving", 
    "allowances", "salaryRaise", "bonus", "holiday", "welfare", "workingHours", 
    "area1name", "category00name", "category01name", "category10name", 
    "category11name", "corporationID", "applicants", "period", "status"
]

foreignKey={"area1.csv":"",
            "category00.csv":"",
            "category01.csv":"",
            "category10.csv":"",
            "category11.csv":"",
            "corporation.csv":"",
            }
basePath='../setup/data/'
for i in foreignKey.keys:
    file_path=makeImportPath(basePath,i)
    value=readFile()


