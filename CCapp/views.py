from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import User, Area0, Area1, Category00, Category01, Category10, Category11, Tag
from .forms import LoginForm
from django.views.generic import TemplateView

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

from .forms import UserUpdateForm
from django.contrib.auth import update_session_auth_hash

class TopView(TemplateView):
    template_name = 'top.html'

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
    success_url = reverse_lazy('CCapp:contact_done')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        message = \
         '送信者名: {0}\nメールアドレス: {1}\n お問い合わせ内容:\n{2}'\
         .format(name, email, message)
        
        from_email = 'admin@example.com'
        to_list = ['tyotyotyo112@gmail.com']
        message = EmailMessage(body=message,
                               from_email=from_email,
                               to=to_list,
                               )
        
        message.send()
        messages.success(
            self.request, 'お問い合わせは正常に送信されました。')
        return super().form_valid(form)
    
class UserUpdateView(FormView):
    template_name = 'account_update.html'  # 使用するテンプレート
    form_class = UserUpdateForm  # 使用するフォーム
    success_url = reverse_lazy('CCapp:profile')  # フォーム送信後にプロフィール画面にリダイレクト

    def get(self, request, *args, **kwargs):
        # ユーザーの現在の情報をフォームにセットして表示
        form = self.form_class(initial={
            'first_name': request.user.first_name,
            'last_name_kana': request.user.last_name_kana,
            'birth_date': request.user.birth_date,
            'gender': request.user.gender,
            'email': request.user.email,
            'phone': request.user.phone,
            'address': request.user.address,
            'school_name': request.user.school_name,
            'department': request.user.department,
            'graduation_year': request.user.graduation_year
        })
        return self.render_to_response({"form": form})

    def form_valid(self, form):
        # フォームが有効な場合、ユーザー情報を更新する処理
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name_kana = form.cleaned_data['last_name_kana']
        user.birth_date = form.cleaned_data['birth_date']
        user.gender = form.cleaned_data['gender']
        user.email = form.cleaned_data['email']
        user.phone = form.cleaned_data['phone']
        user.address = form.cleaned_data['address']

        password = form.cleaned_data.get('password')
        if password:
            user.set_password(password)  # パスワードが変更されていればセットする

        user.school_name = form.cleaned_data['school_name']
        user.department = form.cleaned_data['department']
        user.graduation_year = form.cleaned_data['graduation_year']
        user.save()

        # セッションの認証情報を更新
        update_session_auth_hash(self.request, user)

        messages.success(self.request, 'アカウント情報が更新されました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # フォームが無効な場合、エラーメッセージを表示
        messages.error(self.request, '入力内容に誤りがあります。')
        return super().form_invalid(form)

# accout
# signin
class SigninView(TemplateView):
    template_name = 'signin.html'
# logout
class LogoutView(TemplateView):
    template_name = 'logout.html'
# delete_ac
class Delete_acView(TemplateView):
    template_name = 'delete_ac.html'
# edit_ac
class Edit_acView(TemplateView):
    template_name = 'edit_ac.html'


# profile
class ProfileView(TemplateView):
    template_name = 'profile.html'


# filter
# filter_area
def filter_area_view(request):
    # データベースからエリアの情報を取得
    area0_list = Area0.objects.all()
    area1_list = Area1.objects.all()
    # テンプレートにデータを渡す
    return render(request, 'filter_area.html', {
        'area0_list': area0_list,
        'area1_list': area1_list
    })
# filter_industry
def filter_industry_view(request):
    # データベースから業界の情報を取得
    category00_list = Category00.objects.all()
    category01_list = Category01.objects.all()
    # テンプレートにデータを渡す
    return render(request, 'filter_industry.html', {
        'category00_list': category00_list,
        'category01_list': category01_list
    })
# filter_jobtype
def filter_jobtype_view(request):
    # データベースから職種の情報を取得
    category10_list = Category10.objects.all()
    category11_list = Category11.objects.all()
    # テンプレートにデータを渡す
    return render(request, 'filter_jobtype.html', {
        'category10_list': category10_list,
        'category11_list': category11_list
    })
# filter_benefits
def filter_benefits_view(request):
    # データベースから福利厚生の情報を取得
    tag_list = Tag.objects.all()
    print(tag_list)
    # テンプレートにデータを渡す
    return render(request, 'filter_benefits.html', {'tag_list': tag_list })


# admin
# dashboard
class AdmTopView(TemplateView):
    template_name = 'adm_dashboard.html'
# login
class AdmLoginView(TemplateView):
    template_name = 'adm_login.html'
# post_list
class AdmPostListView(TemplateView):
    template_name = 'adm_post_list.html'


# subscription
class SubscriptionView(TemplateView):
    template_name = 'subscription.html'
# subscription_done
class Subscription_doneView(TemplateView):
    template_name = 'subscription_done.html'


# about
class AboutView(TemplateView):
    template_name = 'about.html'

# jobs
class JobsView(TemplateView):
    template_name = 'jobs.html'


# self
class SelfAnalyView(TemplateView):
    template_name = 'soliloquizing_self_analy.html'