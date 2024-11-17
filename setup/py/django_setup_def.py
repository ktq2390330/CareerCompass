import os
import sys
import django
#Djangoプロジェクトの設定
def djangoSetup():
	project_root=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
	sys.path.append(project_root)
	os.environ.setdefault('DJANGO_SETTINGS_MODULE','CareerCompassProject.settings')
	django.setup()