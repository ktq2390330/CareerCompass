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
class ProfileForm(forms.Form):
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
            self.fields['uname'].initial = self.user.uname
            self.fields['mail'].initial = self.user.mail
            self.fields['birth_date'].initial = self.user.birth_date
            self.fields['gender'].initial = self.user.gender
            self.fields['utel'].initial = self.user.utel
            self.fields['uaddress'].initial = self.user.uaddress
            self.fields['uschool'].initial = self.user.uschool
            self.fields['department'].initial = self.user.department
            self.fields['graduation'].initial = self.user.graduation

    def clean_mail(self):
        mail = self.cleaned_data.get('mail')
        if User.objects.filter(mail=mail).exclude(pk=self.user.pk).exists():
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
            self.user.frigana = self.cleaned_data['frigana']
            self.user.birth_date = self.cleaned_data['birth_date']
            self.user.gender = self.cleaned_data['gender']
            self.user.mail = self.cleaned_data['mail']
            self.user.utel = self.cleaned_data['utel']
            self.user.uaddress = self.cleaned_data['uaddress']
            self.user.uschool = self.cleaned_data['uschool']
            self.user.department = self.cleaned_data['department']
            self.user.graduation = self.cleaned_data['graduation']
            if self.cleaned_data['password']:
                self.user.set_password(self.cleaned_data['password'])
            self.user.save()


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