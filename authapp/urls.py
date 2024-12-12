# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
  
    path('', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='authapp/login.html'), name='login'),
      path('logout/', views.user_logout, name='user_logout'),
]



