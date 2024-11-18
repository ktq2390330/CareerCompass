import sys
from django_setup_def import djangoSetup
djangoSetup()
from django.conf import settings

def configureDBSettings():
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

def configureDebugMode():
    print("\nDebug mode configuration")
    debug=input("Enable DEBUG mode? (yes/no): ").strip().lower()
    settings.DEBUG=debug=='yes'
    print(f"Debug mode set to {settings.DEBUG}.\n")


def configureAllowedHosts():
    print("\nAllowed hosts configuration")
    allowed_hosts=input("Enter allowed hosts (comma-separated): ")
    settings.ALLOWED_HOSTS=[host.strip() for host in allowed_hosts.split(',')]
    print(f"Allowed hosts set to: {settings.ALLOWED_HOSTS}\n")


def configureEmailSettings():
    print("\nEmail settings configuration")
    email_host=input("Enter EMAIL_HOST: ")
    email_port=input("Enter EMAIL_PORT: ")
    email_user=input("Enter EMAIL_HOST_USER: ")
    email_password=input("Enter EMAIL_HOST_PASSWORD: ")
    email_use_tls=input("Use TLS? (yes/no): ").strip().lower()

    settings.EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    settings.EMAIL_HOST=email_host
    settings.EMAIL_PORT=int(email_port)
    settings.EMAIL_HOST_USER=email_user
    settings.EMAIL_HOST_PASSWORD=email_password
    settings.EMAIL_USE_TLS=email_use_tls=='yes'
    print("Email settings updated successfully.\n")


def configureStaticURL():
    print("\nStatic files configuration")
    static_url=input("Enter STATIC_URL: ")
    settings.STATIC_URL=static_url
    print(f"Static files URL set to: {settings.STATIC_URL}\n")


def configureInternationalization():
    print("\nInternationalization configuration")
    language_code=input("Enter LANGUAGE_CODE (e.g., 'en-us', 'ja'): ")
    time_zone=input("Enter TIME_ZONE (e.g., 'UTC', 'Asia/Tokyo'): ")

    settings.LANGUAGE_CODE=language_code
    settings.TIME_ZONE=time_zone
    print(f"Language set to: {settings.LANGUAGE_CODE}, Timezone set to: {settings.TIME_ZONE}\n")


def settingsMenu():
    options={
        '1':configureDBSettings,
        '2':configureDebugMode,
        '3':configureAllowedHosts,
        '4':configureEmailSettings,
        '5':configureStaticURL,
        '6':configureInternationalization,
    }

    while True:
        print("Select the settings to configure:")
        print("1. Database")
        print("2. Debug mode")
        print("3. Allowed hosts")
        print("4. Email")
        print("5. Static files URL")
        print("6. Language and Timezone")
        print("exit. Exit")

        choice=input("Enter the number of your choice: ")

        if choice=='exit':
            print("Exiting configuration.")
            break
        elif choice in options:
            options[choice]()
        else:
            print("Invalid choice. Please try again.\n")

#実行
settingsMenu()