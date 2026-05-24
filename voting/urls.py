from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_voter, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='voting/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('election/<int:election_id>/', views.election_detail, name='election_detail'),
    path('election/<int:election_id>/vote/', views.cast_vote, name='cast_vote'),
    path('election/<int:election_id>/results/', views.election_results, name='results'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
