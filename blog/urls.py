from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('login', views.choice, name='choice'),
    path('login/choice', views.output, name='output'),
    ]
