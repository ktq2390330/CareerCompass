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
    UName = forms.CharField(label='氏名', max_length=255)
    Mail = forms.EmailField(label='メールアドレス')
    Password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    Password_Conf = forms.CharField(label='パスワード確認', widget=forms.PasswordInput())

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
class UserUpdateForm(forms.Form):
    UName = forms.CharField(max_length=30, required=True, label='氏名')
    Frigana = forms.CharField(max_length=30, required=True, label='フリガナ')
    Birth_Date = forms.DateField(required=True, label='生年月日', widget=forms.DateInput(attrs={'type': 'date'}))
    Gender = forms.ChoiceField(choices=[('M', '男性'), ('F', '女性'), ('O', 'その他')], required=True, label='性別')
    Mail = forms.EmailField(required=True, label='メールアドレス')
    UTel = forms.CharField(max_length=15, required=True, label='電話番号')
    UAddress = forms.CharField(max_length=255, required=True, label='住所')
    Password = forms.CharField(widget=forms.PasswordInput, required=False, label='パスワード')
    Password_Conf = forms.CharField(widget=forms.PasswordInput, required=False, label='パスワード確認')
    Uschool = forms.CharField(max_length=100, required=False, label='学校名')
    department = forms.CharField(max_length=100, required=False, label='学部・学科名')
    Graduation = forms.IntegerField(required=False, label='卒業年')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # 初期値をユーザー情報で設定
        if self.user:
            self.fields['UName'].initial = self.user.UName
            self.fields['Mail'].initial = self.user.Mail
            # 他のフィールドも必要に応じて初期値を設定

    def clean_email(self):
        Mail = self.cleaned_data.get('Mail')
        if User.objects.filter(email=Mail).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("このメールアドレスは既に使用されています。")
        return Mail

    def clean(self):
        cleaned_data = super().clean()
        Password = cleaned_data.get('Password')
        Password_Conf = cleaned_data.get('Password_Conf')

        if Password and Password != Password_Conf:
            self.add_error('password_conf', "パスワードが一致しません。")
        
        return cleaned_data

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

class UserUpdateForm(forms.Form):
    uname = forms.CharField(max_length=30, required=True, label='氏名')
    frigana = forms.CharField(max_length=30, required=True, label='フリガナ')
    birth_date = forms.DateField(required=True, label='生年月日', widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('M', '男性'), ('F', '女性'), ('O', 'その他')], required=True, label='性別')
    mail = forms.EmailField(required=True, label='メールアドレス')
    utel = forms.CharField(max_length=15, required=True, label='電話番号')
    uaddress = forms.CharField(max_length=255, required=True, label='住所')
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='パスワード')
    password_conf = forms.CharField(widget=forms.PasswordInput, required=False, label='パスワード確認')
    uschool = forms.CharField(max_length=100, required=False, label='学校名')
    department = forms.CharField(max_length=100, required=False, label='学部・学科名')
    graduation = forms.IntegerField(required=False, label='卒業年')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # 初期値をユーザー情報で設定
        if self.user:
            self.fields['first_name'].initial = self.user.uname
            self.fields['mail'].initial = self.user.mail
            # 他のフィールドも必要に応じて初期値を設定

    def clean_email(self):
        mail = self.cleaned_data.get('mail')
        if User.objects.filter(email=mail).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("このメールアドレスは既に使用されています。")
        return mail

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_conf = cleaned_data.get('password_conf')

        if password and password != password_conf:
            self.add_error('password_conf', "パスワードが一致しません。")
        
        return cleaned_data

    def save(self):
        if self.user:
            self.user.uname = self.cleaned_data['uname']
            self.user.mail = self.cleaned_data['mail']
            # 他のフィールドもユーザーオブジェクトに保存する
            if self.cleaned_data['password']:
                self.user.set_password(self.cleaned_data['password'])
            self.user.save()