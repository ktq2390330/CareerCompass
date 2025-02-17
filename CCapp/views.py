import time
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

@login_required(login_url='CCapp:login') # ログインしていない場合はログインページへ遷移
# トップページのview関数
def top_page_view(request):
    # ユーザーが認証されているか確認する
    if not request.user.is_authenticated:
        print("ユーザーは認証されていません")
    else:
        print(f"認証済みユーザー: {request.user.mail}")

    # データベースからカテゴリとエリア情報を取得する
    category00_list = Category00.objects.all()
    category10_list = Category10.objects.all()
    area1_list = Area1.objects.all()

    # 取得したデータをテンプレートに渡してレンダリング
    return render(request, 'top.html', {
        'category00_list': category00_list,
        'category10_list': category10_list,
        'area1_list': area1_list,
    })

# ログイン処理を担当するビュークラス
class LoginView(FormView):
    template_name = 'login.html' # ログインページのテンプレート
    form_class = LoginForm # 使用するformクラス

    # フォームにrequestを渡すためのメソッド
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request # フォームにリクエストオブジェクトを渡す
        return kwargs

    # フォームのバリデーションが成功した場合の処理
    def form_valid(self, form):
        _mail = form.cleaned_data['mail']
        password = form.cleaned_data['password']
        try:
            # メールアドレスからユーザーｗ検索
            user = User.objects.get(mail=_mail)
        except User.DoesNotExist:
            # メールアドレスまたはユーザーが見つからない場合
            form.add_error(None, 'ユーザー名またはパスワードが正しくありません')
            return self.form_invalid(form)

        # パスワードが一致するかチェックし、パスワードが一致しない場合
        if not user.password == password:
            form.add_error(None, 'ユーザー名またはパスワードが正しくありません')
            return self.form_invalid(form)
        
        # authorityが0（管理者）の場合のみログインを許可
        if user.authority == 2:
            login(self.request, user) # Djangoのログイン処理
            return redirect('CCapp:top') # トップページへリダイレクト
        else:
            # 権限が適切でない場合のエラーメッセージ
            form.add_error(None, 'このアカウントではログインできません。一般ユーザーアカウントでやり直してください。')
            return self.form_invalid(form)


# 新規登録のビュークラス
class SignupView(View):
    def get(self, request):
        # サインアップページを表示
        user_form = SignupForm()
        profile_form = ProfileForm()
        form_list = [user_form, profile_form]  # ✅ ここでリストを作成
        return render(request, "signup.html", {"user_form": user_form, "profile_form": profile_form, "form_list": form_list})

    def post(self, request):
        # フォーム送信時の処理
        user_form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST)
        form_list = [user_form, profile_form]  # ✅ ここでもリストを作成

        if user_form.is_valid() and profile_form.is_valid():
            # フォームデータを取得
            mail = user_form.cleaned_data["mail"] # `mail` を取得
            password = user_form.cleaned_data["password"] # `password` を取得
            name = user_form.cleaned_data["name"]  # `name` を取得
            furigana = profile_form.cleaned_data["furigana"]  # `furigana` を取得

            # メールアドレスが既に存在するか確認
            if User.objects.filter(mail=mail).exists():
                user_form.add_error("mail", "このメールアドレスはすでに使用されています。")
                return render(request, "signup.html", {"user_form": user_form, "profile_form": profile_form})
            
            # User インスタンスを作成（パスワードをハッシュ化せずに保存）
            user = User.objects.create(
                mail=mail,
                password=password,  # パスワードをハッシュ化せずに保存
                name=name,  # `name` に氏名を保存
                authority=2  # 一般ユーザーとして登録
            )

            # Profile インスタンスを作成し、User と関連付ける
            profile = profile_form.save(commit=False) # フォームのデータを取得するが、まだ保存しない
            profile.user = user # Userモデルと関連付ける
            profile.furigana = furigana  # フリガナもプロフィールに保存
            profile.save() # プロフィールを保存

            # ユーザーをログインさせてトップページへリダイレクト
            login(request, user)
            return redirect("CCapp:top")  # ✅ サインアップ後 `top` へ
        # バリデーションエラーがある場合は再表示
        return render(request, "signup.html", {"user_form": user_form, "profile_form": profile_form, "form_list": form_list})

# お問い合わせフォームのビュークラス
class ContactView(LoginRequiredMixin, FormView):
    template_name ='contact.html' # お問い合わせフォームのテンプレート
    form_class = ContactForm # 使用するフォーム
    success_url = reverse_lazy('CCapp:contact_done') # 送信完了後のリダイレクト先
    login_url = 'CCapp:login'  # 必要に応じてログインページのURLを設定

    # フォームのバリデーションが成功した場合の処理
    def form_valid(self, form):
        # フォームのデータを取得
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        # メールの本文を作成
        message = \
        '送信者名: {0}\nメールアドレス: {1}\n お問い合わせ内容:\n{2}'\
        .format(name, email, message)
        
        # 送信元と送信先を設定
        from_email = 'admin@example.com' # 運営側のメールアドレス
        to_list = ['tyotyotyo112@gmail.com'] # 受信者(管理者)
        # メールオブジェクトを作成
        message = EmailMessage(
            body=message,
            from_email=from_email,
            to=to_list,
        )
        
        # メールを送信
        message.send()
        # 送信成功のユーザーメッセージ
        messages.success(
            self.request, 'お問い合わせは正常に送信されました。')
        # 親クラスのform_valid() を実行し、成功時のリダイレクトを行う
        return super().form_valid(form)

# プロフィール編集ページのビュークラス
class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'profile.html' # 使用するテンプレート
    form_class = ProfileForm # 利用するフォーム
    success_url = reverse_lazy('CCapp:profile') # 更新完了後のリダイレクト先
    login_url = 'CCapp:login' # 未ログイン時のリダイレクト先

    def get_initial(self):
        # プロフィールの初期値を設定
        user = self.request.user
        # プロフィールが存在しない場合、新規作成(デフォルト値を設定)
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'birth': '2000-01-01', 'graduation': 25},
        )
        # 初期値用の辞書を取得
        initial = super().get_initial()

        # プロフィールが存在する場合、フィールドに値を設定
        for field in self.form_class.Meta.fields:
            value = getattr(profile, field, None)
            initial[field] = value if value is not None else ''  # Noneの場合は空文字を設定

        # ユーザーの名前を初期値として設定
        initial['name'] = user.name  # Userの名前をフォームの初期値として設定
        initial['furigana'] = profile.furigana if profile.furigana else '' # フリガナの初期値

        return initial

    def form_valid(self, form):
        # フォームが正常に送信された場合、氏名を更新
        user = self.request.user

        # `name` フィールドは ProfileForm に存在しないため、リクエストから直接取得する
        user.name = self.request.POST.get("name", user.name)  # name が送信されていない場合は変更しない
        user.save()

        # プロフィールのデータも更新
        # profile = user.profile
        # profile.birth = form.cleaned_data['birth']
        # profile.graduation = form.cleaned_data['graduation']

        profile = user.profile
        profile.furigana = form.cleaned_data.get("furigana", profile.furigana)
        profile.birth = form.cleaned_data.get("birth", profile.birth)
        profile.gender = form.cleaned_data.get("gender", profile.gender)
        profile.graduation = form.cleaned_data.get("graduation", profile.graduation)
        profile.uSchool = form.cleaned_data.get("uSchool", profile.uSchool)
        profile.uTel = form.cleaned_data.get("uTel", profile.uTel)
        profile.postalCode = form.cleaned_data.get("postalCode", profile.postalCode)
        profile.uAddress = form.cleaned_data.get("uAddress", profile.uAddress)
        profile.save()

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        # テンプレートへ渡すコンテキストデータを追加して返す
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['name'] = user.name  # ユーザー名をコンテキストに渡す
        return context

# アカウント
# サインインページ
class SigninView(LoginRequiredMixin,TemplateView):
    template_name = 'signin.html'
    login_url = 'CCapp:login'

# ログアウト確認ページ
class LogoutConfView(LoginRequiredMixin, TemplateView):
    template_name = 'logout.html'
    login_url = 'CCapp:login'
    
# ログアウト処理
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
    
# アカウント編集画面
class Edit_acView(LoginRequiredMixin, TemplateView):
    template_name = 'edit_ac.html'


def save_to_session(request, key, param_name):
    # GETパラメータを取得してセッションに保存
    if param_name in request.GET:
        request.session[key] = request.GET.getlist(param_name)

# フィルタ画面のviews
def filter_view(request):

    # データベースから各項目のリストを取得
    area0_list = Area0.objects.all() # 地方名
    area1_list = Area1.objects.all() # 県名
    category00_list = Category00.objects.all() # 業界の中分類
    category01_list = Category01.objects.all() # 業界の小分類
    category10_list = Category10.objects.all() # 職種の中分類
    category11_list = Category11.objects.all() # 職種の小分類
    tag_list = Tag.objects.all() # 福利厚生のタグリスト

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
# 求人検索のviews
def offer_search_view(request):
    # 検索条件を取得(GETパラメータからリスト形式で取得)
    filters = {
        'name': request.GET.getlist('name'), # 求人名
        'welfare': request.GET.getlist('welfare'), # 福利厚生
        'area0': request.GET.getlist('area0'), # 地方
        'area1': request.GET.getlist('area1'), # 都道府県
        'category00': request.GET.getlist('category00'), # 業界(中分類)
        'category01': request.GET.getlist('category01'), # 業界(小分類)
        'category10': request.GET.getlist('category10'), # 職種(中分類)
        'category11': request.GET.getlist('category11'), # 職種(小分類)
        'corporation': request.GET.getlist('corporation'), # 法人名
    }
    # デバッグ用に検索条件を出力(本番環境では削除推奨)
    print(filters)

    # ユーザーの権限を取得
    authority = int(request.GET.get("authority", 2))  # デフォルトはユーザー権限（2）
    # フィルタリング関数を呼び出し、求人情報を取得
    offers = filter_offers(filters, authority)

    # ページネーションの設定
    paginator = Paginator(offers, 50)  # 1ページあたり50件表示
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # コンテキストにデータを渡す
    context = {
        'page_obj': page_obj, # ページネーションされた求人情報
        'page_range': paginator.page_range, # ページ番号リスト
        'filters': filters,  # 検索クエリをコンテキストに追加
    }

    return render(request, 'search_result.html', context)

# 管理者
from django.db.models import Q
from django.views.generic import ListView, View
# 管理者ダッシュボード
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

# 管理者ログイン
class AdmLoginView(FormView):
    template_name = 'adm_login.html' # 使用するテンプレート
    form_class = LoginForm # ログインフォーム

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    # フォームが有効な場合の処理
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
            login(self.request, user) # ログイン処理
            return redirect('CCapp:adm_dashboard') # 管理者ダッシュボードへリダイレクト
        else:
            # 管理者権限がない場合はエラーを表示
            form.add_error(None, '管理者権限がありません')
            return self.form_invalid(form)
        
# ログアウト確認画面
class AdmLogoutConfView(LoginRequiredMixin, TemplateView):
    template_name = 'adm_logout.html'

# ログアウト
def AdmLogoutView(request):
    logout(request) # 現在のセッションを終了し、ユーザーをログアウトさせる
    return redirect('CCapp:adm_login') # 管理者ログインページにリダイレク

# 管理者用投稿一覧ページ
class AdmPostListView(TemplateView):
    template_name = 'adm_post_list.html' # 使用するテンプレート
    login_url = 'CCapp:adm_login'


# 求人応募
from django.core.mail import send_mail
from django.contrib import messages
# 求人応募
class SubscriptionView(LoginRequiredMixin, View):
    # 求人応募の確認画面
    def get(self, request, offer_id):
        # 求人IDに基づいてOfferを取得。存在しない場合は404エラー
        offer = get_object_or_404(Offer, id=offer_id)
        # ログインしているユーザーのプロフィール情報を取得、存在しない場合は404エラー
        profile = get_object_or_404(Profile, user=request.user)
        # 求人とプロフィールをテンプレートに渡して確認画面を表示
        return render(request, 'subscription.html', {'offer': offer, 'profile': profile})

class Subscription_doneView(LoginRequiredMixin, View):
    # 求人応募の処理＆完了画面
    def post(self, request, offer_id):
        # 求人IDに基づいてOfferを取得。存在しない場合は404エラー
        offer = get_object_or_404(Offer, id=offer_id)
        # ログインしているユーザーを取得
        user = request.user
        # ユーザーのプロフィール情報を取得。存在しない場合は404エラー
        profile = get_object_or_404(Profile, user=user)

        # 求人に企業情報を取得
        corporation = offer.corporation
        if not corporation:
            # 企業情報が設定されていない場合、エラーメッセージを表示し、求人詳細画面にリダイレクト
            messages.error(request, "企業情報が設定されていません。")
            return redirect('CCapp:offer_detail', offer_id=offer_id)
        
        # 応募処理（ManyToManyに追加）
        offer.applicants.add(user)
        
        # 企業へメール送信
        subject = f"{user.name} 様が {offer.name} に応募しました"
        message = (
            f"この方からの応募がありました。\n\n"
            f"名前: {user.name}\n"
            f"フリガナ: {profile.furigana}\n"
            f"生年月日: {profile.birth}\n"
            f"メールアドレス: {user.mail}\n"
            f"電話番号: {profile.uTel}\n"
            f"住所: {profile.uAddress}\n"
            f"学校名: {profile.uSchool}\n"
            f"卒業年: {profile.graduation}\n\n"
            f"下記メールアドレスから応募者とやり取りを開始してください。\n"
            f"応募者メール: {user.mail}"
        )
        send_mail(subject, message, 'no-reply@example.com', [corporation.cMail])
        
        # 求人応募完了後のページを表示
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

# 自己分析
from .forms import AssessmentForm
from django.db import transaction
from .assessment_filter import run_evaluation

@login_required(login_url='CCapp:login')
# 自己分析ページを表示
def self_analy_view(request):
    # Question00モデルから id=1 の質問タイトルを取得
    question_title_list = Question00.objects.filter(id=1)
    # Question01 モデルから question00_id=1 の質問内容を取得
    self_analy_list = Question01.objects.filter(question00_id=1)

    # セッションから判定結果を取得（初回はNone）
    evaluation_results = request.session.pop('evaluation_results', None)

    """
    AssessmentForm を初期化。質問内容 (self_analy_list)、
    ユーザー (request.user)、そして POST データ（存在すれば）を渡す
    """
    form = AssessmentForm(
        questions=self_analy_list, # 質問内容
        user=request.user, # ユーザー情報
        data=request.POST or None # POSTデータがあればそれを使用、なければNone
    )

    # コンテキストに質問内容、フォーム、判定結果を渡してテンプレートをレンダリング
    return render(request, 'soliloquizing_self_analy.html', {
        'question_title_list': question_title_list, # 質問タイトル
        'self_analy_list': self_analy_list, # 質問内容リスト
        'form': form, # フォームオブジェクト
        'evaluation_results': evaluation_results,  # 判定結果を表示
    })


@login_required(login_url='CCapp:login')
def self_analy_processing(request):
    """判定中の処理を行い、完了後にリダイレクト"""
    if request.method == "POST":
        # Question01 モデルから question00_id=1 の質問内容を取得
        self_analy_list = Question01.objects.filter(question00_id=1)
        
        # ユーザーが回答した内容を辞書形式で取得
        # 各質問の回答は 'answer_<question_id>' という形式でPOSTされる
        # もしユーザーがその質問に答えなかった場合、空文字を代入
        user_answers = {
            question.id: request.POST.get(f'answer_{question.id}', '') # 回答の取得
            for question in self_analy_list
        }

        # AIで評価
        evaluation_results = run_evaluation({request.user.id: user_answers}).get(request.user.id, {})

        # True のものだけを保存
        with transaction.atomic():
            for question in self_analy_list:
                answer_value = request.POST.get(f'answer_{question.id}', '')
                if evaluation_results.get(question.id, False):  # True の場合のみ保存
                    Assessment.objects.update_or_create(
                        user=request.user,
                        question01=question,
                        defaults={'answer': answer_value}
                    )

        # セッションに判定結果を保存し、元のページにリダイレクト
        request.session['evaluation_results'] = evaluation_results
        return redirect('CCapp:self_analy')

    return render(request, 'processing.html')  # GETリクエスト時は判定中画面を表示

# axis
@login_required(login_url='CCapp:login')
def axis_view(request):
    # データベースから質問を取得
    # id=2のQuestion00と、それに紐づくQuestion01を取得
    question_title_list = Question00.objects.filter(id=2)
    axis_list = Question01.objects.filter(question00_id=2)

    # フォームの初期データを動的に設定
    # 「axis_list」の質問内容をフォームに設定し、POSTデータがあればそれも渡す
    form = AssessmentForm(
        questions=axis_list, 
        user=request.user,
        data=request.POST or None  # POSTデータがあれば渡す
    )

    # POSTリクエストが送信された場合
    if request.method == "POST" and form.is_valid():
        # 保存処理
        # フォームが正しく送信されている場合、各質問に対する回答を処理
        for question in axis_list:
            answer_key = f'answer_{question.id}' # 各質問の回答のキーを作成
            if answer_key in form.cleaned_data: # フォームから回答が送信されていれば
                answer_value = form.cleaned_data[answer_key] # 回答の値を取得

                # 既存の回答があれば更新、なければ作成
                Assessment.objects.update_or_create(
                    user=request.user, # ログインユーザー
                    question01=question, # 質問
                    defaults={'answer': answer_value} # 回答内容
                )

        # 回答後、同じページへリダイレクト（自分自身のページをリフレッシュ）
        return redirect('CCapp:axis')
    
    # GETリクエスト時、またはフォームが無効な場合
    return render(request, 'soliloquizing_axis.html', {
        'question_title_list': question_title_list, # 質問のタイトル(Question00)
        'self_analy_list': axis_list, # 質問リスト(Question01)
        'form': form, # フォーム
    })

# industry
@login_required(login_url='CCapp:login')
def industry_view(request):
    # データベースから質問を取得
    # id=3のQuestion00と、それに紐づくQuestion01を取得
    question_title_list = Question00.objects.filter(id=3)
    industry_list = Question01.objects.filter(question00_id=3)

    # フォームの初期データを動的に設定
    # 「industry_list」の質問内容をフォームに設定し、POSTデータがあればそれも渡す
    form = AssessmentForm(
        questions=industry_list, 
        user=request.user,
        data=request.POST or None  # POSTデータがあれば渡す
    )

    # POSTリクエストが送信された場合
    if request.method == "POST" and form.is_valid():
        # 保存処理
        # フォームが正しく送信されている場合、各質問に対する回答を処理
        for question in industry_list:
            answer_key = f'answer_{question.id}' # 各質問の回答のキーを作成
            if answer_key in form.cleaned_data: # フォームから回答が送信されていれば
                answer_value = form.cleaned_data[answer_key] # 回答の値を取得

                # 既存の回答があれば更新、なければ作成
                Assessment.objects.update_or_create(
                    user=request.user, # ログインユーザー
                    question01=question, # 質問
                    defaults={'answer': answer_value} # 回答内容
                )

        # 回答後、同じページへリダイレクト（自分自身のページをリフレッシュ）
        return redirect('CCapp:industry')

    # GETリクエスト時、またはフォームが無効な場合
    return render(request, 'soliloquizing_industry.html', {
        'question_title_list': question_title_list, # 質問のタイトル(Question00)
        'self_analy_list': industry_list, # 質問リスト(Question01)
        'form': form, # フォーム
    })

# jobtype
@login_required(login_url='CCapp:login')
def jobtype_view(request):
    # データベースから質問を取得
    # id=4のQuestion00と、それに紐づくQuestion01を取得
    question_title_list = Question00.objects.filter(id=4)
    jobtype_list = Question01.objects.filter(question00_id=4)

    # フォームの初期データを動的に設定
    # 「jobtype_list」の質問内容をフォームに設定し、POSTデータがあればそれも渡す
    form = AssessmentForm(
        questions=jobtype_list, 
        user=request.user,
        data=request.POST or None  # POSTデータがあれば渡す
    )

    # POSTリクエストが送信された場合
    if request.method == "POST" and form.is_valid():
        # 保存処理
        # フォームが正しく送信されている場合、各質問に対する回答を処理
        for question in jobtype_list:
            answer_key = f'answer_{question.id}' # 各質問の回答のキーを作成
            if answer_key in form.cleaned_data: # フォームから回答が送信されていれば
                answer_value = form.cleaned_data[answer_key] # 回答の値を取得

                # 既存の回答があれば更新、なければ作成
                Assessment.objects.update_or_create(
                    user=request.user, # ログインユーザー
                    question01=question, # 質問
                    defaults={'answer': answer_value} # 回答内容
                )
        # 回答後、同じページへリダイレクト（自分自身のページをリフレッシュ）
        return redirect('CCapp:jobtype')

    # GETリクエスト時、またはフォームが無効な場合
    return render(request, 'soliloquizing_jobtype.html', {
        'question_title_list': question_title_list, # 質問のタイトル(Question00)
        'self_analy_list': jobtype_list, # 質問リスト(Question01)
        'form': form, # フォーム
    })

from django.http import JsonResponse
from .forms import AdmPostForm

class AdmPostView(LoginRequiredMixin, View):
    # 管理者用の求人投稿ページテンプレート
    template_name = 'adm_post.html'

    def get(self, request):
        # GETリクエスト時、空のフォームを表示
        form = AdmPostForm() # 新規フォームのインスタンスを作成
        # テンプレートにフォームを渡してレンダリング
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # POSTリクエスト時、送信されたデータを使ってフォームをインスタンス化
        form = AdmPostForm(request.POST)
        if form.is_valid():
            # 法人情報の保存
            corp = Corporation(
                corp=form.cleaned_data['corp'], # 法人名
                name=form.cleaned_data['name'], # 法人番号
                address=form.cleaned_data['address'], # 住所
                cMail=form.cleaned_data['cMail'], # 企業メールアドレス
                cTel=form.cleaned_data['cTel'], # 電話番号
                url=form.cleaned_data['url'], # 企業のウェブサイトURL
            )
            corp.save()  # 法人情報を保存

            # 求人情報の保存
            offer = form.save(commit=False) # フォームデータで求人情報オブジェクトを作成
            offer.corporation = corp  # 保存した法人情報を関連付け
            offer.save()  # 求人情報を保存

            # 求人情報が正常に保存されたら、投稿完了画面にリダイレクト
            return redirect('CCapp:adm_post_done')  # 投稿完了画面にリダイレクト

        # フォームが無効な場合、再度フォームを表示
        return render(request, self.template_name, {'form': form})

    
# 求人投稿完了のビュー
class AdmPostDoneView(View):
    def get(self, request):
        # 投稿完了画面（'adm_post_done.html'）を表示
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

from django.views.generic.edit import UpdateView
from .forms import OfferEditForm
# # 管理者が求人情報を編集するためのビュークラス
class AdmEditPostView(UpdateView):
    model = Offer # 編集対象となるモデル
    form_class = OfferEditForm # 求人情報を編集するためのフォーム
    template_name = "adm_edit_post.html" # 使用するテンプレート
    context_object_name = "job" # テンプレートに渡す編集対象のオブジェクト

    # フォームが正常に送信された場合、更新後の遷移先URLを返す
    def get_success_url(self):
        messages.success(self.request, f"求人情報 '{self.object.name}' が更新されました。") # 成功メッセージ
        return reverse_lazy("CCapp:adm_post_list") # 求人一覧ページにリダイレクト

    # フォームが無効な場合、エラーメッセージを表示
    def form_invalid(self, form):
        messages.error(self.request, "入力内容に誤りがあります。もう一度確認してください。") # エラーメッセージ
        return super().form_invalid(form)

    # 編集対象のオブジェクトを取得
    def get_object(self, queryset=None):
        return super().get_object(queryset) # 既存の求人情報を取得


from django.shortcuts import get_object_or_404
# 求人詳細ページのビュー
def job_detail(request, id):
    offer = get_object_or_404(Offer, id=id) # 指定されたIDの求人情報を取得
    
    # 認証済みユーザーなら Profile を取得、それ以外は None
    profile = None
    if request.user.is_authenticated: # ユーザーがログインしていれば
        profile = Profile.objects.filter(user=request.user).first() # ユーザーのプロフィールを取得
    
    # エントリー権限がない場合のメッセージ
    show_analysis_message = False
    if profile and not profile.entryAuth: # プロフィールがあり、エントリー権限がない場合
        show_analysis_message = True # メッセージ表示フラグを設定

    # レンダリングして求人詳細ページを表示
    return render(request, 'jobs.html', {
        'offer': offer, # 求人情報
        'profile': profile, # ユーザーのプロフィール
        'show_analysis_message': show_analysis_message # エントリー権限のメッセージ表示フラグ
    })
