from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import User
from .forms import LoginForm

# TemplateViewをインポート
from django.views.generic.base import TemplateView
# FormViewをインポート
from django.views.generic import FormView
# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
# formsモジュールからContactFormをインポート
from .forms import ContactForm
# django.contribからmesseagesをインポート
from django.contrib import messages
# django.core.mailモジュールからEmailMessageをインポート
from django.core.mail import EmailMessage

class IndexView(TemplateView):
    template_name = 'top.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

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
    
class ContactView(FormView):
    template_name ='contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('CCapp:contact')
    
    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['message']
        subject = 'お問い合わせ: {}'.format(title)
        message = \
            'お名前: {0}\nメールアドレス: {1}\n お問い合わせ内容: \n{2}' \
            .format(name, email, message)
        # メールの送信元のメールアドレス
        from_email = 'admin@exxxx.com'
        # 送信先のメールアドレス
        to_list = ['admin@exxx.com']
        message = EmailMessage(subject=subject,
                               body=message,
                               from_email=from_email,
                               to=to_list,
                               )
        message.send()
        message.success(
            self.request, 'お問い合わせは正常に送信されました。')
        return super().form_valid(form)