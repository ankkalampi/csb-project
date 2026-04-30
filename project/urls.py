from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('busted/', views.busted_view, name='busted'),
    path('<str:username>/', views.user_view, name='user'),
]