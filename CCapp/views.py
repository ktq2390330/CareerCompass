from django.shortcuts import render

# TemplateViewをインポート
from django.views.generic.base import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'

class LoginView(TemplateView):
    template_name = 'login.html'