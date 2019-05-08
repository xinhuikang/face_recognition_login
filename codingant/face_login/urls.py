from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('login/loginFaceCheck/', views.loginFaceCheck),
    path('update/', views.update),
    path('action_detect/', views.face_action_detect),
    path('action_detect/eye_blink_detect/', views.eye_blink_detect),
    path('action_detect/month_open_detect/', views.month_open_detect),
]
