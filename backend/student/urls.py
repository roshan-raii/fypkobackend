from django.urls import path
from .views import *
urlpatterns=[
    path('login/',StudentLogin.as_view()),
    path('forgot/',StudentForgotPassword.as_view())
]