import sys
from django_setup_def import djangoSetup
djangoSetup()
from django.conf import settings

def updateSettings():
	while True:
		print("Select the setting:\n1. DB\nexit. Exiting the program")
		choice=input("Your choice: ")
		if choice=='1':
			updateDBSettings()
		elif choice=="exit":
			print("Exiting the program.")
			sys.exit()
		else:
			print("Invalid choice. Exiting the program.")
			sys.exit()

def updateDBSettings():
	print("Select the database engine:\n1. MySQL\n2. PostgreSQL\n3. SQLite\n4. Oracle\n5. MariaDB\n6. Microsoft SQL Server")
	if engine=='1':
		engine='django.db.backends.mysql'
	elif engine=='2':
		engine='django.db.backends.postgresql'
	elif engine=='3':
		engine='django.db.backends.sqlite3'
	elif engine=='4':
		engine='django.db.backends.oracle'
	elif engine=='5':
		engine='django.db.backends.mysql'
	elif engine=='6':
		engine='sql_server.pyodbc'
	else:
		print("Invalid choice. Defaulting to MySQL.")
		engine='django.db.backends.mysql'
	engine=input("Your engine: ")
	name=input("NAME: ")
	user=input("USER: ")
	password=input("PASSWORD: ")
	host=input("HOST: ")
	port=input("PORT: ")
	settings.DATABASES['default']={
        'ENGINE': f'{engine}',
        'NAME': f'{name}',
        'USER': f'{user}',
        'PASSWORD': f'{password}',
        'HOST': f'{host}',
        'PORT': f'{port}',
    }
	print(settings.DATABASES['default'])

#実行
updateSettings()