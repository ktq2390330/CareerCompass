from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

#新規登録
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserSignupForm(forms.Form):
    uname = forms.CharField(max_length=30, required=True, label='氏名')
    furigana = forms.CharField(max_length=30, required=True, label='フリガナ')
    
    # 生年月日を年、月、日の3つのフィールドに分ける
    birth_date_year = forms.IntegerField(required=True, label='生年')
    birth_date_month = forms.IntegerField(required=True, label='生月')
    birth_date_day = forms.IntegerField(required=True, label='生日')

    # 性別をラジオボタンとその他のフィールドで入力
    gender_choices = [('M', '男性'), ('F', '女性')]
    gender = forms.ChoiceField(choices=gender_choices, required=False, widget=forms.RadioSelect, label='性別')
    gender_other = forms.CharField(max_length=30, required=False, label='その他の性別', widget=forms.TextInput(attrs={'placeholder': 'その他を入力'}))
    
    mail = forms.EmailField(required=True, label='メールアドレス')
    utel = forms.CharField(max_length=15, required=True, label='電話番号')
    uaddress = forms.CharField(max_length=255, required=True, label='住所')
    uschool = forms.CharField(max_length=100, required=False, label='学校名')
    department = forms.CharField(max_length=100, required=False, label='学部・学科名')
    graduation = forms.IntegerField(required=False, label='卒業年')
    
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='パスワード')
    password_conf = forms.CharField(widget=forms.PasswordInput(), required=True, label='パスワード確認')
    
    def clean_email(self):
        mail = self.cleaned_data.get('email')
        if User.objects.filter(mail=mail).exists():
            raise forms.ValidationError("このメールアドレスは既に使われています。")
        return mail
    
    def clean_password_confirmation(self):
        password = self.cleaned_data.get('Password')
        password_conf = self.cleaned_data.get('Password_Conf')
        if password != password_conf:
            raise forms.ValidationError("パスワードが一致しません。")
        return password_conf
    
    def clean(self):
        cleaned_data = super().clean()
        # 生年月日のチェック（年、月、日が全て入力されているか確認）
        if cleaned_data.get('birth_date_year') and cleaned_data.get('birth_date_month') and cleaned_data.get('birth_date_day'):
            birth_date = f"{cleaned_data['birth_date_year']}-{cleaned_data['birth_date_month']:02d}-{cleaned_data['birth_date_day']:02d}"
            cleaned_data['birth_date'] = birth_date
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
            self.user.mail = self.cleaned_data['mail']
            # 他のフィールドもユーザーオブジェクトに保存する
            if self.cleaned_data['password']:
                self.user.set_password(self.cleaned_data['password'])
            self.user.save()