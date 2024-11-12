from django.urls import path
from . import views


urlpatterns = [
    path('', views.front_page, name='home'),
    path('register/', views.Register_user, name='register'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logout, name='logout'),
]