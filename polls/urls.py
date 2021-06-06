from django.contrib import admin
from django.urls import include, path
from polls import views

urlpatterns = [
    path('{id}/', views.index),
]
