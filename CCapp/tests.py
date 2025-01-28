from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your tests here.
User = get_user_model()

# class UserManagerTests(TestCase):
#     def setUp(self):
#         self.mail = 'test@example.com'
#         self.password = 'password123'

#     def test_create_user(self):
#         user = User.objects.create_user(mail=self.mail, password=self.password)
#         self.assertEqual(user.mail, self.mail)
#         self.assertTrue(user.check_password(self.password))

#     def test_create_superuser(self):
#         superuser = User.objects.create_superuser(mail=self.mail, password=self.password)
#         self.assertEqual(superuser.mail, self.mail)
#         self.assertTrue(superuser.check_password(self.password))
#         # self.assertTrue(superuser.is_superuser)
#         # self.assertTrue(superuser.is_staff)

#     def test_create_user_without_mail(self):
#         with self.assertRaises(ValueError):
#             User.objects.create_user(mail='', password=self.password)

#     def test_create_user_with_extra_fields(self):
#         user = User.objects.create_user(mail=self.mail, password=self.password, username='testuser')
#         self.assertEqual(user.username, 'testuser')

class LoginViewTest(TestCase):
    def setUp(self):
        self.mail = 'admin@master.com'
        self.password = 'password'
        self.user = User.objects.create_user(mail=self.mail, password=self.password)
        self.login_url = reverse('CCapp:login')

    def test_login_with_valid_credentials(self):
        """正しい資格情報でログインできるかをテスト"""
        response = self.client.post(self.login_url, {
            'mail': self.mail,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('CCapp:top'))

    # def test_login_with_invalid_credentials(self):
    #     """無効な資格情報でログインできないかをテスト"""
    #     response = self.client.post(self.login_url, {
    #         'mail': self.mail,
    #         'password': 'wrongpassword',
    #     })
    #     self.assertContains(response, 'ユーザー名またはパスワードが正しくありません')

    # def test_login_with_nonexistent_user(self):
    #     """存在しないユーザーでログインできないかをテスト"""
    #     response = self.client.post(self.login_url, {
    #         'mail': 'nonexistent@example.com',
    #         'password': 'password123',
    #     })
    #     self.assertContains(response, 'ユーザー名またはパスワードが正しくありません')

# class LogoutViewTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
#         self.login_url = reverse('login')
#         self.logout_url = reverse('logout')

#     def test_logout(self):
#         """ログイン後、ログアウトできるかをテスト"""
#         # ログイン
#         self.client.login(username='testuser', password='password123')

#         # ログアウトリクエスト
#         response = self.client.get(self.logout_url)
#         self.assertRedirects(response, '/')  # ログアウト後のリダイレクト先を確認

#         # ユーザーがログアウト状態か確認
#         response = self.client.get(reverse('CCapp:top'))
#         self.assertNotIn('_auth_user_id', self.client.session)


# class SignupViewTest(TestCase):

#     def setUp(self):
#         self.signup_url = reverse('signup')  # サインアップURLを名前で取得

#     def test_signup_page(self):
#        response = self.client.get(self.signup_url)
#        self.assertEqual(response.status_code, 200)
#        self.assertTemplateUsed(response, 'signup.html')