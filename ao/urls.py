from django.contrib import admin
from django.urls import include, path


from . import views

urlpatterns = [
   path('', views.home, name="home"),
   path('resavation/', views.reservation, name="resa"),
   path('contact/', views.contact, name="contact"),
   path('example/', views.example, name='example'),
   path('example_confirm/', views.example_confirm, name='example_confirm'),
   path('example_fix/', views.example_fix, name='example_fix'),

]