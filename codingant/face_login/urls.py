from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('login/loginFaceCheck/', views.loginFaceCheck),
    path('update/', views.update),
    path('test/', views.test),
]
