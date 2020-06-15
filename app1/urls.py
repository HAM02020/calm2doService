from django.urls import path
from rest_framework import routers

from . import views


urlpatterns = [
    path('register',views.Register.as_view()),
    path('login',views.Login.as_view()),
    path('beginjx',views.BeginJx.as_view()),
    path('endjx',views.EndJx.as_view()),
    path('jxinfo',views.JXInfo.as_view()),
]
