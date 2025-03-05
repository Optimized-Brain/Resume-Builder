from django.urls import path
from . import views

app_name = 'resume'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_resume, name='create_resume'),
    path('view/', views.view_resume, name='view_resume'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),
    path('logout/', views.logout_view, name='logout'),
]
