from django import forms
from django.contrib.auth.models import User

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
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='パスワード')
    password_conf = forms.CharField(widget=forms.PasswordInput, required=False, label='パスワード確認')

    class Meta:
        model = Profile
        fields = [
            'furigana', 'nationality', 'birth', 'gender', 'graduation', 
            'uSchool', 'sClass', 'sol', 'department', 'uTel', 
            'postalCode', 'uAddress', 'category00', 'category01', 
            'category10', 'category11', 'area1', 'uOffer'
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
        }
        widgets = {
            'birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # `user` を取得
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_conf = cleaned_data.get('password_conf')

        if password and password != password_conf:
            self.add_error('password_conf', "パスワードが一致しません。")

        return cleaned_data
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user and self.cleaned_data.get('password'):
            self.user.set_password(self.cleaned_data['password'])
            if commit:
                self.user.save()
        if commit:
            profile.save()
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