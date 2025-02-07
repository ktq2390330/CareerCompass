from django import forms
from django.contrib.auth.models import User
from .models import *

class LoginForm(forms.Form):
    mail = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # 'request'を取り除いて処理
        super().__init__(*args, **kwargs)

# サインアップフォーム
class SignupForm(forms.Form):
    mail = forms.EmailField(label="メールアドレス", required=True)
    name = forms.CharField(label="氏名", max_length=64, required=True)
    password = forms.CharField(
        label="パスワード", 
        widget=forms.PasswordInput(), 
        required=True
    )

    def save(self):
        # create_user メソッドを使ってユーザーを作成
        user = User.objects.create_user(
            username=self.cleaned_data["mail"],  # mailをusernameとして使用
            email=self.cleaned_data["mail"],     # 同じくemailとしても使用
            password=self.cleaned_data["password"]
        )
        return user

# プロフィール登録フォーム
class ProfileForm(forms.ModelForm):
    furigana = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Profile
        fields = [
            "furigana", "birth", "gender", "graduation",
            "uSchool", "uTel", "postalCode", "uAddress"
        ]
        labels = {
            "furigana": "フリガナ",  # ここで正しいラベルを設定
            "birth": "生年月日",
            "gender": "性別",
            "graduation": "卒業年度",
            "uSchool": "学校名",
            "uTel": "電話番号",
            "postalCode": "郵便番号",
            "uAddress": "住所",
        }

        widgets = {
            "birth": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "uTel": forms.TextInput(attrs={"placeholder": "例: 09012345678"}),
            "postalCode": forms.TextInput(attrs={"placeholder": "例: 123-4567"}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(label='お名前')
    email = forms.EmailField(label='メールアドレス')
    message = forms.CharField(label='お問い合わせ内容', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # nameフィールドのplaceholderにメッセージを登録
        self.fields['name'].widget.attrs['placeholder'] = \
        'お名前を入力してください'
        # nameフィールドを出力する<input>タグのclass属性を設定
        self.fields['name'].widget.attrs['class'] = 'form-control'

        # emailフィールドのplaceholderにメッセージを登録
        self.fields['email'].widget.attrs['placeholder'] = \
        'メールアドレスを入力してください'
        # emailフィールドを出力する<input>タグのclass属性を設定
        self.fields['email'].widget.attrs['class'] = 'form-control'

        # messageフィールドのplaceholderにメッセージを登録
        self.fields['message'].widget.attrs['placeholder'] = \
        'お問い合わせ内容を入力してください'
        # messageフィールドの出力する<input>タグのclass属性を設定
        self.fields['message'].widget.attrs['class'] = 'form-control'

    # メールアドレスが正しい形式かチェック
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("正しいメールアドレスの形式で入力してください。")
        return email

class AssessmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions')  # 質問リストを受け取る
        self.user = kwargs.pop('user')  # 現在のユーザーを受け取る
        super().__init__(*args, **kwargs)

        # 動的にフィールドを追加
        for question in self.questions:
            # ユーザーの回答を取得（もし存在すれば）
            existing_answer = Assessment.objects.filter(user=self.user, question01=question).first()
            initial_value = existing_answer.answer if existing_answer else ""

            # フィールドを追加
            self.fields[f'answer_{question.id}'] = forms.CharField(
                label=f'Q{question.id}: {question.name}',  # 質問番号をラベルに含める
                widget=forms.Textarea(attrs={
                    'rows': 2,
                    'id': f'Q{question.id}',  # 質問番号をidとして設定
                }),
                initial=initial_value,
                required=False
            )

class AdmPostForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'name', 'detail', 'solicitation', 'course', 'forms', 'roles',
            'CoB', 'subject', 'NoP', 'departments', 'characteristic', 'PES',
            'giving', 'allowances', 'salaryRaise', 'bonus', 'holiday',
            'workingHours', 'area1', 'category00', 'category01',
            'category10', 'category11', 'corporation', 'period', 'status', 'welfare'
        ]

        welfare = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label="福利厚生",
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # カテゴリ01をカテゴリ00に基づいて動的に変更
        if 'category00' in self.data:
            try:
                category00_id = int(self.data.get('category00'))
                self.fields['category01'].queryset = Category01.objects.filter(category00_id=category00_id)
            except (ValueError, TypeError):
                self.fields['category01'].queryset = Category01.objects.none()
        else:
            self.fields['category01'].queryset = Category01.objects.none()

        # カテゴリ11をカテゴリ10に基づいて動的に変更
        if 'category10' in self.data:
            try:
                category10_id = int(self.data.get('category10'))
                self.fields['category11'].queryset = Category11.objects.filter(category10_id=category10_id)
            except (ValueError, TypeError):
                self.fields['category11'].queryset = Category11.objects.none()
        else:
            self.fields['category11'].queryset = Category11.objects.none()

        # エリアのラベルを都道府県名のみ表示
        self.fields['area1'].label_from_instance = lambda obj: obj.name.split('-')[-1]

        # カテゴリ00、カテゴリ10、福利厚生（タグ）のリストを設定
        self.fields['category00'].queryset = Category00.objects.all()
        self.fields['category10'].queryset = Category10.objects.all()
        self.fields['welfare'].queryset = Tag.objects.all()

        # カテゴリ00とカテゴリ10の選択肢をnameで表示
        self.fields['category00'].label_from_instance = lambda obj: obj.name
        self.fields['category10'].label_from_instance = lambda obj: obj.name

        # 福利厚生タグの表示をnameで設定
        self.fields['welfare'].label_from_instance = lambda obj: obj.name

class OfferEditForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'name', 'detail', 'solicitation', 'course', 'forms', 'roles',
            'CoB', 'subject', 'NoP', 'departments', 'characteristic', 'PES',
            'giving', 'allowances', 'salaryRaise', 'bonus', 'holiday',
            'workingHours', 'area1', 'category00', 'category01',
            'category10', 'category11', 'period', 'status', 'welfare'
        ]

    welfare = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label="福利厚生",
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # カテゴリ01とカテゴリ11をすべて表示
        self.fields['category01'].queryset = Category01.objects.all()
        self.fields['category11'].queryset = Category11.objects.all()

        # エリアのラベルを都道府県名のみ表示
        self.fields['area1'].label_from_instance = lambda obj: obj.name.split('-')[-1]

        # カテゴリ00、カテゴリ10、福利厚生（タグ）のリストを設定
        self.fields['category00'].queryset = Category00.objects.all()
        self.fields['category10'].queryset = Category10.objects.all()
        self.fields['welfare'].queryset = Tag.objects.all()

        # カテゴリ00、カテゴリ10、カテゴリ01、カテゴリ11の選択肢をnameで表示
        self.fields['category00'].label_from_instance = lambda obj: obj.name
        self.fields['category10'].label_from_instance = lambda obj: obj.name
        self.fields['category01'].label_from_instance = lambda obj: obj.name
        self.fields['category11'].label_from_instance = lambda obj: obj.name

        # 福利厚生タグの表示をnameで設定
        self.fields['welfare'].label_from_instance = lambda obj: obj.name

