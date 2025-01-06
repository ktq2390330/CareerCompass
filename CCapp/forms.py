from django import forms
from django.contrib.auth.models import User
from .models import Assessment

class LoginForm(forms.Form):
    mail = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # 'request'を取り除いて処理
        super().__init__(*args, **kwargs)

# サインアップ（新規登録）フォーム
from django.core.exceptions import ValidationError
from .models import User

class SignupForm(forms.Form):
    # フィールド定義
    UName = forms.CharField(label='氏名', max_length=255, required=True)
    Mail = forms.EmailField(label='メールアドレス', required=True)
    Password = forms.CharField(label='パスワード', widget=forms.PasswordInput(), required=True)
    Password_Conf = forms.CharField(label='パスワード確認', widget=forms.PasswordInput(), required=True)

    # バリデーション
    def clean_Mail(self):
        mail = self.cleaned_data.get('Mail')
        if User.objects.filter(mail=mail).exists():
            raise forms.ValidationError('このメールアドレスはすでに使用されています。')
        return mail

    def clean_Password_Conf(self):
        password = self.cleaned_data.get('Password')
        password_conf = self.cleaned_data.get('Password_Conf')

        if password != password_conf:
            raise forms.ValidationError('パスワードと確認用パスワードが一致しません。')
        return password_conf

# プロフィール更新用フォーム
from .models import Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'furigana', 'nationality', 'birth', 'gender', 'graduation', 
            'uSchool', 'sClass', 'sol', 'department', 'uTel', 
            'postalCode', 'uAddress', 'category00', 'category01', 
            'category10', 'category11', 'area1', 'uOffer', 'photo'
        ]
        labels = {
            'furigana': 'フリガナ',
            'nationality': '国籍',
            'birth': '生年月日',
            'gender': '性別',
            'graduation': '卒業年度',
            'uSchool': '学校名',
            'sClass': '学校区分',
            'sol': '文理区分',
            'department': '学科名',
            'uTel': '電話番号',
            'postalCode': '郵便番号',
            'uAddress': '住所',
            'category00': 'カテゴリ00',
            'category01': 'カテゴリ01',
            'category10': 'カテゴリ10',
            'category11': 'カテゴリ11',
            'area1': 'エリア1',
            'uOffer': '内定先',
            'photo': 'プロフィール写真'
        }
        widgets = {
            'birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'graduation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'uTel': forms.TextInput(attrs={'placeholder': '例: 09012345678'}),
            'postalCode': forms.TextInput(attrs={'placeholder': '例: 123-4567'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # 必須フィールドの確認
        if not cleaned_data.get('graduation'):
            self.add_error('graduation', "卒業年度は必須です。")

        if not cleaned_data.get('birth'):
            self.add_error('birth', "生年月日は必須です。")

        return cleaned_data
    
    def clean_graduation(self):
        graduation_date = self.cleaned_data.get('graduation')
        if graduation_date:
            return graduation_date.year  # 年の部分のみを返す
        return None
    
    def save(self, commit=True):
        profile = super().save(commit=commit)
        return profile


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

            self.fields[f'answer_{question.id}'] = forms.CharField(
                label=f'Q: {question.name}',
                widget=forms.Textarea(attrs={'rows': 2}),  # style属性を削除
                initial=initial_value,
                required=False
            )
