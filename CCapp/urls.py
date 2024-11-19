from django.urls import path
from . import views

app_name = 'CCapp'

urlpatterns = [
    # top
    path('', views.TopView.as_view(), name='top'),

    # account
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signin/', views.SigninView.as_view(), name='signin'),

    # contact
    path('contact/',views.ContactView.as_view(), name='contact'),

    # profile
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # filter
    path('filter_area/', views.filter_area_view, name='filter_area'),
    path('filter_industry/',views.filter_industry_view, name='filter_industry'),
    path('filter_jobtype/',views.filter_jobtype_view, name='filter_jobtype'),
    path('filter_benefits/',views.filter_benefits_view, name='filter_benefits'),

    # admin
    path('adm_dashboard/', views.AdmTopView.as_view(), name='adm_dashboard'),
    path('adm_login/', views.AdmLoginView.as_view(), name='adm_login'),
    path('adm_logout/', views.AdmLogoutView.as_view(), name='adm_logout'),
    path('adm_post_list/', views.AdmPostListView.as_view(), name='adm_post_list'),

    # subscription
    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
    path('subscription_done/', views.Subscription_doneView.as_view(), name='subscription_done'),

    # about
    path('about/', views.AboutView.as_view(), name='about'),

    # jobs
    path('jobs/', views.JobsView.as_view(), name='jobs'),

    # search
    path('search_result/', views.Search_resultView.as_view(), name='search_result'),

    # self
    path('self_analy/', views.SelfAnalyView.as_view(), name='self_analy'),
    path('axis/', views.AxisView.as_view(), name='axis'),
    path('industry/', views.IndustryView.as_view(), name='industry'),
    path('jobtype/', views.JobtypeView.as_view(), name='jobtype'),
]