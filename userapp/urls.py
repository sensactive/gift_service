from django.urls import path

import userapp.views as userapp

app_name='userapp'

urlpatterns = [
    path('login/', userapp.login, name='login'),
    path('logout/', userapp.logout, name='logout'),
    path('register/', userapp.register, name='register'),
    path('edit/', userapp.edit, name='edit'),
    path('verify/<int:pk>/<str:activation_key>/', userapp.verify, name='verify'),
    path('loginar/', userapp.login_after_registration, name='login_a_r')
]