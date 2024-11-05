from django.urls import path
from . import views

app_name = 'CCapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('contact/',views.contact_view, name='contact'),
]