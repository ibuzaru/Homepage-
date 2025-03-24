from django.contrib import admin
from django.urls import include, path


from . import views

urlpatterns = [
   path('', views.home, name="home"),
   path('resavation/', views.reservation, name="resa"),
   path('example/', views.example, name='example'),
   path('example_confirm/', views.example_confirm, name='example_confirm'),
   path('example_fix/', views.example_fix, name='example_fix'),
   path('success_reserve/', views.success_reserve, name='success_reserve'),
   path('rooms', views.rooms, name="rooms"),
   path('faq/', views.faq, name="faq"),
   path('access/', views.supermarket, name='supermarket'),
   path('sightseeing/', views.sightseeing, name="sightseeing"),
   path('howtostay/', views.howtostay, name="howtostay"),
   path('kiyaku/', views.kiyaku, name="kiyaku"),
]