from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

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
    first_name = forms.CharField(max_length=30, required=True, label='氏名')
    last_name_kana = forms.CharField(max_length=30, required=True, label='フリガナ')
    birth_date = forms.DateField(required=True, label='生年月日', widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('M', '男性'), ('F', '女性'), ('O', 'その他')], required=True, label='性別')
    email = forms.EmailField(required=True, label='メールアドレス')
    phone = forms.CharField(max_length=15, required=True, label='電話番号')
    address = forms.CharField(max_length=255, required=True, label='住所')
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='パスワード')
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=False, label='パスワード確認')
    school_name = forms.CharField(max_length=100, required=False, label='学校名')
    department = forms.CharField(max_length=100, required=False, label='学部・学科名')
    graduation_year = forms.IntegerField(required=False, label='卒業年')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # 初期値をユーザー情報で設定
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['email'].initial = self.user.email
            # 他のフィールドも必要に応じて初期値を設定

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("このメールアドレスは既に使用されています。")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password != password_confirm:
            self.add_error('password_confirm', "パスワードが一致しません。")
        
        return cleaned_data

    def save(self):
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.email = self.cleaned_data['email']
            # 他のフィールドもユーザーオブジェクトに保存する
            if self.cleaned_data['password']:
                self.user.set_password(self.cleaned_data['password'])
            self.user.save()