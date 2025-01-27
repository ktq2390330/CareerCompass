from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('filter_base/', views.filter_view, name='filter_base'),
    path('filter_area/', views.filter_area_view, name='filter_area'),
    path('filter_industry/',views.filter_industry_view, name='filter_industry'),
    path('filter_jobtype/',views.filter_jobtype_view, name='filter_jobtype'),
    path('filter_benefits/',views.filter_benefits_view, name='filter_benefits'),

    # admin
    path('adm_dashboard/', views.AdmTopView.as_view(), name='adm_dashboard'),
    path('adm_login/', views.AdmLoginView.as_view(), name='adm_login'),
    path('adm_logout_conf/', views.AdmLogoutConfView.as_view(), name='adm_logout_conf'),
    path('adm_logout/', views.AdmLogoutView, name='adm_logout'),
    path('search/', views.AdmPostList.as_view(), name='adm_post_list'),
    path('adm_post/', views.AdmPostView.as_view(), name='adm_post'),
    path('get_category01/<int:category00_id>/', views.get_category01_options, name='get_category01'),
    path('get_category11/<int:category10_id>/', views.get_category11_options, name='get_category11'),
    path('get_area/<str:area1_name>/', views.get_area_options, name='get_area'),
    path('adm_post_done/', views.AdmPostDoneView.as_view(), name='adm_post_done'),
    path("edit_job/<int:pk>/", views.AdmEditPostView.as_view(), name="edit_job"),
    path('search/', views.AdmPostList.as_view(), name='adm_post_list'),
    path('post/<int:pk>/delete/', views.AdmPostDelView.as_view(), name='adm_post_del'),  # 削除確認画面
    path('post/<int:pk>/delete/done/', views.AdmPostDelDoneView.as_view(), name='adm_post_del_done'),  # 削除完了画面

    # subscription
    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
    path('subscription_done/', views.Subscription_doneView.as_view(), name='subscription_done'),

    # about
    path('about/', views.AboutView.as_view(), name='about'),

    # jobs
    path('jobs/', views.JobsView.as_view(), name='jobs'),

    # search
    # path('search_result/', views.search_result_view, name='search_result'),
    path('offer_search/', views.offer_search_view, name='offer_search'),
    path('offer/<int:id>/', views.job_detail, name='job_detail'),

    # self
    path('self_analy/', views.self_analy_view, name='self_analy'),
    path('axis/', views.axis_view, name='axis'),
    path('industry/', views.industry_view, name='industry'),
    path('jobtype/', views.jobtype_view, name='jobtype'),
    path('save_answer/', views.save_answer_view, name='save_answer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)