from django.urls import path
from . import views

app_name = 'CCapp'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('contact/',views.contact_view, name='contact'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]