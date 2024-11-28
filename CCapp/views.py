from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import *
from .forms import LoginForm
from django.views.generic import TemplateView
from django.views import View
from .forms import SignupForm
from django.contrib.auth import logout
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

from .forms import ProfileForm
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='CCapp:login')
def top_page_view(request):
    if not request.user.is_authenticated:
        print("ユーザーは認証されていません")
    else:
        print(f"認証済みユーザー: {request.user.mail}")

    category00_list = Category00.objects.all()
    category10_list = Category10.objects.all()
    area1_list = Area1.objects.all()

    return render(request, 'top.html', {
        'category00_list': category00_list,
        'category10_list': category10_list,
        'area1_list': area1_list,
    })

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        _mail = form.cleaned_data['mail']
        password = form.cleaned_data['password']
        try:
            user = User.objects.get(mail=_mail)
        except User.DoesNotExist:
            # メールアドレスが見つからない場合
            form.add_error(None, 'ユーザー名またはパスワードが正しくありません')
            return self.form_invalid(form)

        # パスワードが一致しない場合
        if not user.password == password:
            form.add_error(None, 'ユーザー名またはパスワードが正しくありません')
            return self.form_invalid(form)

        login(self.request, user)
        return redirect('CCapp:top')


# 新規登録のviews
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data.get('Mail')  # 'Mail' フィールドを取得
            password = form.cleaned_data.get('Password')
            name = form.cleaned_data.get('UName')

            # 'mail' を使用してユーザーを作成
            # パスワードをハッシュ化せずに保存（後にハッシュ化できるようにする）
            user = User.objects.create(mail=mail, password=password)
            # user = User.objects.create_user(mail=mail, password=password)
            user.name = name  # 名前を 'name' フィールドに保存
            user.save()

            # 自動ログイン
            login(request, user)

            messages.success(request, '新規登録が完了しました。')
            return redirect('CCapp:top')  # トップページにリダイレクト

        else:
            messages.error(request, '入力に誤りがあります。')

        return render(request, 'signup.html', {'form': form})

class ContactView(LoginRequiredMixin, FormView):
    template_name ='contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('CCapp:contact_done')
    login_url = 'CCapp:login'  # 必要に応じてログインページのURLを設定

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
    
class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'profile.html'  # 使用するテンプレート
    form_class = ProfileForm  # 使用するフォーム
    success_url = reverse_lazy('CCapp:profile')  # フォーム送信後のリダイレクトURL
    login_url = 'CCapp:login'  # ログインが必要な場合のリダイレクトURL

    def get_form_kwargs(self):
        """
        フォームの初期化時にユーザー情報を渡す
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.profile  # プロフィール情報を渡す
        return kwargs

    def form_valid(self, form):
        """
        フォームが有効な場合、ユーザー情報を更新
        """
        user = self.request.user
        profile = user.profile

        # フォームのデータでユーザー情報を更新
        for field, value in form.cleaned_data.items():
            if field == "password" and value:
                user.set_password(value)  # パスワードは特別に処理
            elif field != "password_conf":
                setattr(profile, field, value)  # 他のフィールドはそのままセット

        # パスワードが変更されている場合、セッションを更新
        if form.cleaned_data.get("password"):
            user.save()
            update_session_auth_hash(self.request, user)

        # プロフィールを保存
        profile.save()

        messages.success(self.request, 'アカウント情報が更新されました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        フォームが無効な場合
        """
        messages.error(self.request, '入力内容に誤りがあります。')
        return super().form_invalid(form)
    
# accout
# signin
class SigninView(LoginRequiredMixin,TemplateView):
    template_name = 'signin.html'
    login_url = 'CCapp:login'

# logout_conf
class LogoutConfView(LoginRequiredMixin, TemplateView):
    template_name = 'logout.html'
    login_url = 'CCapp:login'
    
# logout
def LogoutView(request):
    logout(request)
    return redirect('CCapp:login')
# delete_ac
class Delete_acView(LoginRequiredMixin, TemplateView):
    template_name = 'delete_ac.html'
# edit_ac
class Edit_acView(LoginRequiredMixin, TemplateView):
    template_name = 'edit_ac.html'

# filter
# filter_area
@login_required(login_url='CCapp:login')
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
@login_required(login_url='CCapp:login')
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
@login_required(login_url='CCapp:login')
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
@login_required(login_url='CCapp:login')
def filter_benefits_view(request):
    # データベースから福利厚生の情報を取得
    tag_list = Tag.objects.all()
    # テンプレートにデータを渡す
    return render(request, 'filter_benefits.html', {'tag_list': tag_list })


# admin
# dashboard
class AdmTopView(TemplateView):
    template_name = 'adm_dashboard.html'
    login_url = '#'
# login
class AdmLoginView(FormView):
    template_name = 'adm_login.html'
    form_class = LoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        _mail = form.cleaned_data['mail']
        password = form.cleaned_data['password']
        try:
            user = User.objects.get(mail=_mail)
        except User.DoesNotExist:
            # メールアドレスが見つからない場合
            form.add_error(None, 'ユーザー名またはパスワードが正しくありません')
            return self.form_invalid(form)

        # パスワードの不一致
        if not user.password == password:
            form.add_error(None, 'ユーザー名またはパスワードが正しくありません')
            return self.form_invalid(form)
        
        # authorityが0（管理者）の場合のみログインを許可
        if user.authority == 0:
            login(self.request, user)
            return redirect('CCapp:adm_dashboard')
        else:
            form.add_error(None, '管理者権限がありません')
            return self.form_invalid(form)

# logout_conf

# logout
class AdmLogoutView(TemplateView):
    template_name = 'adm_logout.html'
    login_url = '#'
# post_list
class AdmPostListView(TemplateView):
    template_name = 'adm_post_list.html'
    login_url = '#'


# subscription
class SubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = 'subscription.html'
    login_url = 'CCapp:login'
# subscription_done
class Subscription_doneView(LoginRequiredMixin, TemplateView):
    template_name = 'subscription_done.html'
    login_url = 'CCapp:login'


# about
class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'
    login_url = 'CCapp:login'

# jobs
class JobsView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs.html'
    login_url = 'CCapp:login'

# search
class SearchresultView(LoginRequiredMixin, TemplateView):
    template_name = 'search_result.html'
    login_url = 'CCapp:login'


# self
class SelfAnalyView(LoginRequiredMixin, TemplateView):
    template_name = 'soliloquizing_self_analy.html'
    login_url = 'CCapp:login'

class AxisView(LoginRequiredMixin, TemplateView):
    template_name = 'soliloquizing_axis.html'
    login_url = 'CCapp:login'

class IndustryView(LoginRequiredMixin, TemplateView):
    template_name = 'soliloquizing_industry.html'
    login_url = 'CCapp:login'

class JobtypeView(LoginRequiredMixin, TemplateView):
    template_name = 'soliloquizing_jobtype.html'
    login_url = 'CCapp:login'

class AdmPostView(LoginRequiredMixin, TemplateView):
    template_name = 'adm_post.html'
    login_url = '#'

class AdmPostDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'adm_post_done.html'
    login_url = '#'

class AdmEditPostView(LoginRequiredMixin, TemplateView):
    template_name = 'adm_edit_post.html'
    login_url = '#'