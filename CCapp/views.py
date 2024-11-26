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

from .forms import UserUpdateForm
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

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
            user = User.objects.get(mail=_mail, password=password)
        except User.DoesNotExist:
            form.add_error(None, 'ユーザー名またはパスワードが正しくありません')
            return self.form_invalid(form)

        login(self.request, user)
        # 'top' という名前でURLをリダイレクト
        return redirect('CCapp:top')


# 新規登録のviews
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            # フォームからメールアドレスとパスワードを取得
            cleaned_data = form.cleaned_data
            mail = cleaned_data["Mail"]
            password = cleaned_data["Password"]

            # ユーザーを作成
            user = User.objects.get_or_create(
                mail=mail,
                password=password,  # パスワードはハッシュ化していない
            )
            

            # 作成したユーザーIDを取得
            user_id = user.id

            # プロフィール情報を設定（フォームの他のフィールドを使用）
            user.first_name = cleaned_data["UName"]
            user.last_name_kana = cleaned_data["Furigana"]
            user.birth_date = f'{cleaned_data["Birth_Date_Year"]}年{cleaned_data["Birth_Date_Month"]}月{cleaned_data["Birth_Date_Day"]}日'
            user.gender = cleaned_data["Gender_Other"] if cleaned_data["Gender"] == "Other" else cleaned_data["Gender"]
            user.phone = cleaned_data["UTel"]
            user.address = cleaned_data["UAddress"]
            user.school_name = cleaned_data["USchool"]
            user.department = cleaned_data["Department"]
            user.graduation_year = cleaned_data["Graduation"]
            # ユーザーを自動でログイン
            login(request, user)

            # メッセージを表示
            messages.success(request, "新規登録が完了しました！")

            # トップページにリダイレクト
            return redirect("CCapp:top")
        else:
            return render(request, ".../signup/", {"form": form})


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
    
class UserUpdateView(LoginRequiredMixin, FormView):
    template_name = 'account_update.html'  # 使用するテンプレート
    form_class = UserUpdateForm  # 使用するフォーム
    success_url = reverse_lazy('CCapp:profile')  # フォーム送信後にプロフィール画面にリダイレクト
    login_url = 'CCapp:login'  # ログインが必要な場合のリダイレクトURL

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
class SigninView(LoginRequiredMixin,TemplateView):
    template_name = 'signin.html'
    login_url = 'CCapp:login'
# logout
class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'logout.html'
    login_url = 'CCapp:login'
# delete_ac
class Delete_acView(LoginRequiredMixin, TemplateView):
    template_name = 'delete_ac.html'
# edit_ac
class Edit_acView(LoginRequiredMixin, TemplateView):
    template_name = 'edit_ac.html'


# profile
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = 'CCapp:login'

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
class AdmLoginView(TemplateView):
    template_name = 'adm_login.html'
    login_url = '#'
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