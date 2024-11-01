from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import User
from .forms import LoginForm

# TemplateViewをインポート
from django.views.generic.base import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'

class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return self.render_to_response({"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data["mail"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(mail=mail)
                if user.password == password:  #簡易的なパスワードチェックを実行
                    login(request, user)
                    return redirect("home")  #ログイン後のリダイレクト先を指定する
                else:
                    messages.error(request, "パスワードが正しくありません。")
            except User.DoesNotExist:
                messages.error(request, "ユーザーが存在しません。")
        return self.render_to_response({"form": form})