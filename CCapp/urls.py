from django.urls import path
from . import views

app_name = 'CCapp'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('contact/',views.ContactView.as_view(), name='contact'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]