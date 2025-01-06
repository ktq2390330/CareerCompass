from django.urls import path
from . import views

app_name = 'CCapp'

urlpatterns = [
    # top
    path('top/', views.top_page_view, name='top'),
    

    # account
    path('', views.LoginView.as_view(), name='login'),
    path('logout_conf/', views.LogoutConfView.as_view(), name='logout_conf'),
    path('logout/', views.LogoutView, name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('delete_ac/', views.Delete_acView.as_view(), name='delete_ac'),
    path('delete_done/', views.Delete_ac_doneView.as_view(), name='delete_done'),

    # contact
    path('contact/',views.ContactView.as_view(), name='contact'),
    path('contact/done/', views.ContactView.as_view(template_name='contact_done.html'), name='contact_done'),

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
    path('adm_logout_conf/', views.AdmLogoutConfView.as_view(), name='adm_logout_conf'),
    path('adm_logout/', views.AdmLogoutView, name='adm_logout'),
    path('adm_post_list/', views.AdmPostListView.as_view(), name='adm_post_list'),
    path('adm_post/', views.AdmPostView.as_view(), name='adm_post'),
    path('adm_post_done/', views.AdmPostDoneView.as_view(), name='adm_post_done'),
    path('adm_edit_post/', views.AdmEditPostView.as_view(), name='adm_edit_post'),

    # subscription
    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
    path('subscription_done/', views.Subscription_doneView.as_view(), name='subscription_done'),

    # about
    path('about/', views.AboutView.as_view(), name='about'),

    # jobs
    path('jobs/', views.JobsView.as_view(), name='jobs'),

    # search
    path('search_result/', views.SearchresultView.as_view(), name='search_result'),

    # self
    path('self_analy/', views.self_analy_view, name='self_analy'),
    path('save_answer/', views.save_analy_view, name='save_answer'),
    path('axis/', views.axis_view, name='axis'),
    path('industry/', views.IndustryView.as_view(), name='industry'),
    path('jobtype/', views.JobtypeView.as_view(), name='jobtype'),
]