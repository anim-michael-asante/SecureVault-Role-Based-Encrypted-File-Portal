from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('toggle-user/<int:user_id>/', views.toggle_user, name='toggle_user'),
]
