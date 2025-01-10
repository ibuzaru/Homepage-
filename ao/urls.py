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
   path('logout/', views.logout_view, name='logout'),
   path('reservation/change/<int:reservation_id>/', views.re_reserve, name='re_reserve'),
   path('reservation/update/<int:reservation_id>/', views.reservation_change, name='reservation_change'),
]