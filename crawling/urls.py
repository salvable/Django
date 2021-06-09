# https://cholol.tistory.com/468?category=739855 참고


# #urls.py
from django.conf.urls import url, include
from django.urls import path
from crawling import views

urlpatterns = [
    path('addStorks/', views.addStorks)
]