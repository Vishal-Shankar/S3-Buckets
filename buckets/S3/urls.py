from django.contrib import admin
from django.urls import path,include
from S3 import views

urlpatterns = [
    path('',views.Buck,name='Buck'),
]
