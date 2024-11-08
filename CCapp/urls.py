from django.urls import path
from . import views

app_name = 'CCapp'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('contact/',views.ContactView.as_view(), name='contact'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('filter_area/',views.Filter_areaView.as_view(), name='filter_area'),
    path('adm_base/', views.AdmBaseView.as_view(), name='adm_base'),
    path('adm_dashboard/', views.AdmTopView.as_view(), name='adm_dashboard'),
    path('adm_login/', views.AdmLoginView.as_view(), name='adm_login'),
]