from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import *
from .forms import LoginForm
from django.views.generic import TemplateView
from django.views import View
from .forms import SignupForm
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db import DatabaseError
from django.db import IntegrityError
from .forms import ProfileForm

from django.contrib.auth.decorators import login_required
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
        
        # authorityが0（管理者）の場合のみログインを許可
        if user.authority == 2:
            login(self.request, user)
            return redirect('CCapp:top')
        else:
            form.add_error(None, 'このアカウントではログインできません。一般ユーザーアカウントでやり直してください。')
            return self.form_invalid(form)


# 新規登録のviews
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            furigana = form.cleaned_data.get('furigana')
            birth = form.cleaned_data.get('birth')
            gender = form.cleaned_data.get('gender')
            postalCode = form.cleaned_data.get('postalCode')
            uAddress = form.cleaned_data.get('uAddress')
            uTel = form.cleaned_data.get('uTel')
            uSchool = form.cleaned_data.get('uSchool')
            graduation = form.cleaned_data.get('graduation')
            mail = form.cleaned_data.get('mail')  # メールアドレスを取得
            password = form.cleaned_data.get('password')  # パスワードを取得

            try:
                # ユーザーを作成
                user = User.objects.create_user(
                    mail=mail,
                    password=password,
                    name=furigana,
                    authority=2  # 権限を設定（必要に応じて変更）
                )

                # 自動ログイン
                login(request, user)

                messages.success(request, '新規登録が完了しました。')
                return redirect('CCapp:top')  # トップページにリダイレクト

            except IntegrityError:
                messages.error(request, 'このメールアドレスはすでに使用されています。')
                return render(request, 'signup.html', {'form': form})

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
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'birth': '2000-01-01', 'graduation': 25},
        )

        print(f"DEBUG: get_initial() -> Profile created: {created}, birth: {profile.birth}")

        initial = super().get_initial()
        
        # プロフィールが存在する場合、フィールドに値を設定
        for field in self.form_class.Meta.fields:
            value = getattr(profile, field, None)
            initial[field] = value if value is not None else ''  # Noneの場合は空文字を設定

        if profile.birth is None:
            initial['birth'] = '2000-01-01'  # 🔥 birth が None の場合はデフォルト値をセット
        
        return initial

    

    def form_valid(self, form):
        profile = form.save(commit=False)  # 保存を一旦抑制
        profile.user = self.request.user  # ユーザーをセット
        profile.save()  # 保存
        messages.success(self.request, 'プロフィール情報が更新されました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        フォームが無効な場合
        """
        messages.error(self.request, '入力内容に誤りがあります。')
        return super().form_invalid(form)
# account
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


def save_to_session(request, key, param_name):
    if param_name in request.GET:
        request.session[key] = request.GET.getlist(param_name)

# filter_base_view
def filter_view(request):

    # データベースから各項目のリストを取得
    area0_list = Area0.objects.all()
    area1_list = Area1.objects.all()
    category00_list = Category00.objects.all()
    category01_list = Category01.objects.all()
    category10_list = Category10.objects.all()
    category11_list = Category11.objects.all()
    tag_list = Tag.objects.all()

    return render(request, 'filter.html', {
        'area0_list': area0_list, # 地方名
        'area1_list': area1_list, # 県名
        'category00_list': category00_list, # 業界の中分類
        'category01_list': category01_list, # 業界の小分類
        'category10_list': category10_list, # 職種の中分類
        'category11_list': category11_list, # 職種の小分類
        'tag_list': tag_list # 福利厚生の条件
    })

from django.core.paginator import Paginator
from .filters import filter_offers

@login_required(login_url='CCapp:login')
def offer_search_view(request):

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

    print(filters)

    authority = int(request.GET.get("authority", 2))  # デフォルトはユーザー権限（2）
    offers = filter_offers(filters, authority)

    # ページネーションの設定
    paginator = Paginator(offers, 50)  # 1ページあたり50件表示
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # コンテキストにデータを渡す
    context = {
        'page_obj': page_obj,
        'page_range': paginator.page_range,
        'filters': filters,  # 検索クエリをコンテキストに追加
    }

    return render(request, 'search_result.html', context)

# admin
from django.db.models import Q
from django.views.generic import ListView, View
# dashboard
class AdmTopView(LoginRequiredMixin, ListView):
    model = Offer
    template_name = 'adm_dashboard.html'
    context_object_name = 'offers'
    def get_queryset(self):
        return Offer.objects.none()  # クエリがない場合は何も表示しない
    
# 検索結果
class AdmPostList(LoginRequiredMixin, ListView):
    model = Offer
    template_name = 'adm_post_list.html'
    context_object_name = 'jobs'  # コンテキストに渡す求人情報の名前
    paginate_by = 50  # 1ページあたり50件表示

    def get_queryset(self):
        query = self.request.GET.get('query', '')  # 検索クエリを取得
        queryset = Offer.objects.filter(status=1)  # 公開状態（status=1）の求人のみ取得

        if query:
            if query.isdigit():  # クエリが数字の場合（法人番号での検索）
                queryset = queryset.filter(
                    Q(corporation__corp=query)  # 法人番号でフィルタリング
                )
            else:  # クエリが文字列の場合（企業名での検索）
                queryset = queryset.filter(
                    Q(corporation__name__icontains=query)  # 企業名を部分一致でフィルタリング
                )
        return queryset  # 最終的な検索結果を返す

    def get_context_data(self, **kwargs):
        # 基本的なコンテキスト情報を取得
        context = super().get_context_data(**kwargs)
        
        # ページネーション情報を取得
        paginator = context['page_obj'].paginator
        current_page = context['page_obj'].number  # 現在のページ番号
        total_pages = paginator.num_pages  # 総ページ数

        # ページ番号を現在のページを中心に前後2ページを表示するように設定
        page_range = []
        for num in range(1, total_pages + 1):
            # 現在のページを中心に前後2ページと、1ページ目・最後のページを表示
            if abs(num - current_page) <= 2 or num == 1 or num == total_pages:
                page_range.append(num)
            # 現在のページから3ページ離れたページに省略記号を表示
            elif num == current_page - 3 or num == current_page + 3:
                page_range.append('...')  # 省略記号

        # ページ番号範囲をコンテキストに追加
        context['page_range'] = page_range
        # 検索クエリ（query）をコンテキストに追加（ページ遷移時にクエリを保持するため）
        context['query'] = self.request.GET.get('query', '')  # デフォルトは空文字

        return context
    
# 求人削除
class AdmPostDelView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # 求人を取得して削除確認ページを表示
        job = get_object_or_404(Offer, pk=pk)
        return render(request, 'adm_post_del.html', {'offer': job})  # 確認画面のテンプレートを表示

    def post(self, request, pk):
        # 削除処理
        job = get_object_or_404(Offer, pk=pk)
        job.status = 0  # ステータスを「削除済み」に変更
        job.save()
        return redirect('CCapp:adm_post_del_done', pk=pk)  # 完了画面にリダイレクト

# 削除完了画面
class AdmPostDelDoneView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'adm_post_del_done.html')  # 削除完了画面を表示

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
from django.core.mail import send_mail
from django.contrib import messages
# subscription
class SubscriptionView(LoginRequiredMixin, View):
    """
    求人応募の確認画面
    """
    def get(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
        profile = get_object_or_404(Profile, user=request.user)
        return render(request, 'subscription.html', {'offer': offer, 'profile': profile})

class Subscription_doneView(LoginRequiredMixin, View):
    """
    求人応募の処理＆完了画面
    """
    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
        user = request.user
        profile = get_object_or_404(Profile, user=user)

        # 企業情報を取得
        corporation = offer.corporation
        if not corporation:
            messages.error(request, "企業情報が設定されていません。")
            return redirect('CCapp:offer_detail', offer_id=offer_id)
        
        # 応募処理（ManyToManyに追加）
        offer.applicants.add(user)
        
        # 企業へメール送信
        subject = f"{user.name} 様が {offer.name} に応募しました"
        message = (
            f"この方からの応募がありました。\n\n"
            f"名前: {profile.furigana}\n"
            f"メール: {user.mail}\n"
            f"電話番号: {profile.uTel}\n"
            f"学校名: {profile.uSchool}\n\n"
            f"下記メールアドレスから応募者とやり取りを開始してください。\n"
            f"応募者メール: {user.mail}"
        )
        send_mail(subject, message, 'no-reply@example.com', [corporation.cMail])
        
        return render(request, 'subscription_done.html', {
            'offer': offer,
            'corporation': corporation,
            'corporation_mail': corporation.cMail
        })

# about
class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'
    login_url = 'CCapp:login'

# jobs
class JobsView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs.html'
    login_url = 'CCapp:login'

# self_analy
from .forms import AssessmentForm  # 必要であればフォームを使う
from .assessment_filter import run_evaluation

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

    # POSTリクエスト処理
    if request.method == "POST" and form.is_valid():
        # 回答データの準備
        assessment_data = {request.user.id: {}}
        for question in self_analy_list:
            answer_key = f'answer_{question.id}'
            if answer_key in form.cleaned_data:
                answer_value = form.cleaned_data[answer_key]
                assessment_data[request.user.id][question.id] = answer_value

        # 評価関数の呼び出し
        evaluation_results = run_evaluation(assessment_data)

        # 保存処理
        errors = []
        for question_id, is_valid in evaluation_results.get(request.user.id, {}).items():
            if is_valid is True:
                Assessment.objects.update_or_create(
                    user=request.user,
                    question01_id=question_id,
                    defaults={'answer': assessment_data[request.user.id][question_id]}
                )
            else:
                errors.append(f"質問ID {question_id} の回答は不適切と判断されました。")

        if errors:
            return render(request, 'soliloquizing_self_analy.html', {
                'question_title_list': question_title_list,
                'self_analy_list': self_analy_list,
                'form': form,
                'errors': errors  # エラーメッセージを渡す
            })

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

from django.http import JsonResponse
from .forms import AdmPostForm

class AdmPostView(LoginRequiredMixin,View):
    template_name = 'adm_post.html'

    def get(self, request):
        form = AdmPostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AdmPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CCapp:adm_post_done')  # 投稿完了画面にリダイレクト
        return render(request, self.template_name, {'form': form})
    
# 求人投稿完了のビュー
class AdmPostDoneView(View):
    def get(self, request):
        return render(request, 'adm_post_done.html')

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

from django.views.generic.edit import UpdateView
from .forms import OfferEditForm
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Offer

class AdmEditPostView(UpdateView):
    model = Offer
    form_class = OfferEditForm
    template_name = "adm_edit_post.html"
    context_object_name = "job"

    def get_success_url(self):
        messages.success(self.request, f"求人情報 '{self.object.name}' が更新されました。")
        return reverse_lazy("CCapp:adm_post_list")

    def form_invalid(self, form):
        messages.error(self.request, "入力内容に誤りがあります。もう一度確認してください。")
        return super().form_invalid(form)


from django.shortcuts import get_object_or_404

def job_detail(request, id):
    offer = get_object_or_404(Offer, id=id)
    return render(request, 'jobs.html', {'offer': offer})