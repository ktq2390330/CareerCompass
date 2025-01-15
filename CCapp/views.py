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
from django.db import DatabaseError

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
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('CCapp:profile')
    login_url = 'CCapp:login'

    def get_initial(self):
        """
        初期値を設定
        """
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        initial = super().get_initial()
        for field in self.form_class.Meta.fields:
            initial[field] = getattr(profile, field, None)
        return initial

    def form_valid(self, form):
        profile = form.save(commit=False)  # 保存を一旦抑制
        profile.user = self.request.user  # ユーザーをセット
        if self.request.FILES.get('photo'):  # 画像がアップロードされている場合
            profile.photo = self.request.FILES['photo']
        profile.save()  # 保存
        messages.success(self.request, 'プロフィール情報が更新されました。')
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

# アカウント削除確認画面と処理
class Delete_acView(View):
    def get(self, request):
        # アカウント削除確認画面を表示
        return render(request, 'delete_ac.html')

    def post(self, request):
        action = request.POST.get('action')

        if action == 'yes':  # ユーザーが「はい」を選択した場合
            try:
                user = request.user
                user.delete()  # アカウント削除処理
                logout(request)  # ログアウトしてセッションを削除
                return redirect('CCapp:delete_done')  # 完了画面へリダイレクト

            except DatabaseError:
                # データベースエラーの場合のエラーメッセージ
                messages.error(request, 'エラーが発生しました。再試行してください。', extra_tags='delete_error')
            except Exception:
                # 予期しないエラーの場合のエラーメッセージ
                messages.error(request, '予期しないエラーが発生しました。', extra_tags='delete_error')

            return redirect('CCapp:delete_ac')  # 削除確認画面に戻る

        elif action == 'no':  # ユーザーが「いいえ」を選択した場合
            return redirect('CCapp:top')  # トップページにリダイレクト


# アカウント削除完了画面
class Delete_ac_doneView(View):
    def get(self, request):
        return render(request, 'delete_done.html')
    
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
from django.db.models import Q
from django.views.generic import ListView
from .models import Offer, Corporation

class AdmTopView(ListView):
    model = Offer
    template_name = 'adm_dashboard.html'
    context_object_name = 'offers'

    def get_queryset(self):
        query = self.request.GET.get('query', '')  # 検索クエリを取得
        if query:
            # queryが数字かどうかを判定し、法人番号として検索する
            if query.isdigit():
                # 法人番号（corp）を文字列として検索
                return Offer.objects.filter(
                    Q(name__icontains=query) | Q(corporation__corp=query)
                )
            else:
                # 企業名に対して部分一致検索（法人名でも検索）
                return Offer.objects.filter(
                    Q(name__icontains=query) | Q(corporation__name__icontains=query)
                )
        return Offer.objects.all()  # クエリがない場合は全ての求人情報を表示

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
class AdmLogoutConfView(LoginRequiredMixin, TemplateView):
    template_name = 'adm_logout.html'
# logout
def AdmLogoutView(request):
    logout(request)
    return redirect('CCapp:adm_login')

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



# soliloquizing
# self_analy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question00, Question01, Assessment
from .forms import AssessmentForm  # 必要であればフォームを使う

@login_required(login_url='CCapp:login')
def self_analy_view(request):
    # データベースから質問を取得
    question_title_list = Question00.objects.filter(id=1)
    self_analy_list = Question01.objects.filter(question00_id=1)

    # フォームの初期データを動的に設定
    form = AssessmentForm(
        questions=self_analy_list, 
        user=request.user,
        data=request.POST or None  # POSTデータがあれば渡す
    )

    if request.method == "POST" and form.is_valid():
        # 保存処理
        for question in self_analy_list:
            answer_key = f'answer_{question.id}'
            if answer_key in form.cleaned_data:
                answer_value = form.cleaned_data[answer_key]

                # 既存の回答があれば更新、なければ作成
                Assessment.objects.update_or_create(
                    user=request.user,
                    question01=question,
                    defaults={'answer': answer_value}
                )

        return redirect('CCapp:self_analy')

    return render(request, 'soliloquizing_self_analy.html', {
        'question_title_list': question_title_list,
        'self_analy_list': self_analy_list,
        'form': form,
    })


# axis
@login_required(login_url='CCapp:login')
def axis_view(request):
    # データベースから質問を取得
    question_title_list = Question00.objects.filter(id=2)
    axis_list = Question01.objects.filter(question00_id=2)

    # フォームの初期データを動的に設定
    form = AssessmentForm(
        questions=axis_list, 
        user=request.user,
        data=request.POST or None  # POSTデータがあれば渡す
    )

    if request.method == "POST" and form.is_valid():
        # 保存処理
        for question in axis_list:
            answer_key = f'answer_{question.id}'
            if answer_key in form.cleaned_data:
                answer_value = form.cleaned_data[answer_key]

                # 既存の回答があれば更新、なければ作成
                Assessment.objects.update_or_create(
                    user=request.user,
                    question01=question,
                    defaults={'answer': answer_value}
                )

        return redirect('CCapp:axis')
    
    return render(request, 'soliloquizing_axis.html', {
        'question_title_list': question_title_list,
        'self_analy_list': axis_list,
        'form': form,
    })

# industry
@login_required(login_url='CCapp:login')
def industry_view(request):
    # データベースから質問を取得
    question_title_list = Question00.objects.filter(id=3)
    industry_list = Question01.objects.filter(question00_id=3)

    # フォームの初期データを動的に設定
    form = AssessmentForm(
        questions=industry_list, 
        user=request.user,
        data=request.POST or None  # POSTデータがあれば渡す
    )

    if request.method == "POST" and form.is_valid():
        # 保存処理
        for question in industry_list:
            answer_key = f'answer_{question.id}'
            if answer_key in form.cleaned_data:
                answer_value = form.cleaned_data[answer_key]

                # 既存の回答があれば更新、なければ作成
                Assessment.objects.update_or_create(
                    user=request.user,
                    question01=question,
                    defaults={'answer': answer_value}
                )

        return redirect('CCapp:industry')

    return render(request, 'soliloquizing_industry.html', {
        'question_title_list': question_title_list,
        'self_analy_list': industry_list,
        'form': form,
    })

# jobtype
@login_required(login_url='CCapp:login')
def jobtype_view(request):
    # データベースから質問を取得
    question_title_list = Question00.objects.filter(id=4)
    jobtype_list = Question01.objects.filter(question00_id=4)

    # フォームの初期データを動的に設定
    form = AssessmentForm(
        questions=jobtype_list, 
        user=request.user,
        data=request.POST or None  # POSTデータがあれば渡す
    )

    if request.method == "POST" and form.is_valid():
        # 保存処理
        for question in jobtype_list:
            answer_key = f'answer_{question.id}'
            if answer_key in form.cleaned_data:
                answer_value = form.cleaned_data[answer_key]

                # 既存の回答があれば更新、なければ作成
                Assessment.objects.update_or_create(
                    user=request.user,
                    question01=question,
                    defaults={'answer': answer_value}
                )

        return redirect('CCapp:jobtype')

    return render(request, 'soliloquizing_jobtype.html', {
        'question_title_list': question_title_list,
        'self_analy_list': jobtype_list,
        'form': form,
    })

@login_required(login_url='CCapp:login')
def save_answer_view(request):
    # データベースから自己分析の情報を取得
    question_title_list = Question00.objects.filter(id=1)  # 特定のquestion_idに絞る
    self_analy_list = Question01.objects.filter(question00_id=1)  # question_idが1のデータを取得

    if request.method == "POST":
        # POSTデータから回答を保存
        for key, value in request.POST.items():
            if key.startswith("answer_"):
                question_id = key.split("_")[1]  # フォームの名前から質問IDを取得
                try:
                    question01 = Question01.objects.get(id=question_id)
                    # 既存の回答がある場合は更新、なければ作成
                    Assessment.objects.update_or_create(
                        user=request.user,
                        question01=question01,
                        defaults={'answer': value.strip()}
                    )
                except Question01.DoesNotExist:
                    # 質問が存在しない場合はスキップ
                    continue

        # 保存後に再表示
        return redirect("CCapp:self_analy")

    # GETリクエスト: 初期データを設定（既に保存された回答があれば、それをフォームに表示）
    initial_data = {}
    for question in self_analy_list:
        assessment = Assessment.objects.filter(user=request.user, question01=question).first()
        if assessment:
            initial_data[question.id] = assessment.answer if assessment.answer is not None else ""  # 保存された回答を初期値に設定

    form = AssessmentForm(initial=initial_data)

    # テンプレートにデータを渡す
    return render(request, 'soliloquizing_self_analy.html', {
        'question_title_list': question_title_list,
        'self_analy_list': self_analy_list,
        'form': form,  # フォームも渡す
    })

from django.http import JsonResponse
from .forms import AdmPostForm
from .models import Offer, Category01, Category11
from django.shortcuts import render, get_object_or_404

class AdmPostView(View):
    template_name = 'adm_post.html'

    def get(self, request):
        form = AdmPostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AdmPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adm_dashboard')  # 管理者ダッシュボードにリダイレクト
        return render(request, self.template_name, {'form': form})

def get_category01_options(request, category00_id):
    """カテゴリ00に関連するカテゴリ01を取得"""
    categories = Category01.objects.filter(category00_id=category00_id).values('id', 'name')
    return JsonResponse({'category01': list(categories)})

def get_category11_options(request, category10_id):
    """カテゴリ10に関連するカテゴリ11を取得"""
    categories = Category11.objects.filter(category10_id=category10_id).values('id', 'name')
    return JsonResponse({'category11': list(categories)})

def get_area_options(request, area1_id):
    """エリアの都道府県を取得"""
    area = get_object_or_404(Area1, pk=area1_id)
    return JsonResponse({'area': area.name.split('-')[-1]})

class AdmPostDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'adm_post_done.html'
    login_url = '#'

class AdmEditPostView(LoginRequiredMixin, TemplateView):
    template_name = 'adm_edit_post.html'
    login_url = '#'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Offer, Area0, Area1, Category00, Category01, Category10, Category11, Tag, Corporation
from .filters import filter_offers

@login_required(login_url='CCapp:login')
def offer_search_view(request):
    # フィルタ条件を取得
    filters = {
        'name': request.GET.getlist('name'),
        'welfare': request.GET.getlist('welfare'),
        'area0': request.GET.getlist('area0'),
        'area1': request.GET.getlist('area1'),
        'category00': request.GET.getlist('category00'),
        'category01': request.GET.getlist('category01'),
        'category10': request.GET.getlist('category10'),
        'category11': request.GET.getlist('category11'),
        'corporation': request.GET.getlist('corporation'),
    }

    # ユーザー権限を取得（管理者または一般ユーザー）
    authority = getattr(request.user, 'authority', None)  # authorityフィールドが存在しない場合に対応

    # Offerモデルをフィルタリング
    offers = filter_offers(filters, authority) if 'filter_offers' in globals() else Offer.objects.filter(status=True)

    # ページネーション処理（1ページに50件表示）
    paginator = Paginator(offers, 50)  # 1ページに50件表示
    page_number = request.GET.get('page', 1)  # デフォルトページを1に設定
    page_obj = paginator.get_page(page_number)

    # 表示するページ番号を5件以内に制限
    current_page = page_obj.number
    total_pages = paginator.num_pages
    start_page = max(current_page - 2, 1)
    end_page = min(current_page + 2, total_pages)
    page_range = range(start_page, end_page + 1)

    # 絞り込み項目リストを取得
    area0_list = Area0.objects.all()
    area1_list = Area1.objects.all()
    category00_list = Category00.objects.all()
    category01_list = Category01.objects.all()
    category10_list = Category10.objects.all()
    category11_list = Category11.objects.all()
    tag_list = Tag.objects.all()
    corporation_list = Corporation.objects.all()

    return render(request, 'search_result.html', {
        'page_obj': page_obj,
        'page_range': page_range,
        'area0_list': area0_list,
        'area1_list': area1_list,
        'category00_list': category00_list,
        'category01_list': category01_list,
        'category10_list': category10_list,
        'category11_list': category11_list,
        'tag_list': tag_list,
        'corporation_list': corporation_list,
    })

from django.shortcuts import render, get_object_or_404
from .models import Offer

def job_detail(request, id):
    offer = get_object_or_404(Offer, id=id)
    return render(request, 'jobs.html', {'offer': offer})