from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
   path('', views.home, name="home"),
   path('resavation/', views.reservation, name="resa"),
   path('example/', views.example, name='example'),
   path('example_confirm/', views.example_confirm, name='example_confirm'),
   path('example_fix/', views.example_fix, name='example_fix'),
   path('mypage/', views.mypage, name="mypage"),
   path('login/', views.login_view, name='login'),
   path('rooms', views.rooms, name="rooms"),
   path('faq/', views.faq, name="faq"),
   path('supermarket/', views.supermarket, name='supermarket'),
   path('sightseeing/', views.sightseeing, name="sightseeing"),
   path('river_info/', views.river_info, name="river_info"),
   path('howtostay/', views.howtostay, name="howtostay"),
]