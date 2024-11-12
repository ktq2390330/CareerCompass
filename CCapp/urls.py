from django.urls import path
from . import views

app_name = 'CCapp'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('contact/',views.ContactView.as_view(), name='contact'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('filter_area/',views.Filter_AreaView.as_view(), name='filter_area'),
    path('filter_benefits/',views.Filter_BenefitsView.as_view(), name='filter_benefits'),
    path('filter_industry/',views.Filter_IndustryView.as_view(), name='filter_industry'),
    path('adm_base/', views.AdmBaseView.as_view(), name='adm_base'),
    path('adm_dashboard/', views.AdmTopView.as_view(), name='adm_dashboard'),
    path('adm_login/', views.AdmLoginView.as_view(), name='adm_login'),
    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
    path('subscription_done/', views.Subscription_doneView.as_view(), name='subscription_done'),
    path('signin/', views.SigninView.as_view(), name='signin'),
]