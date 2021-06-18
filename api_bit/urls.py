# #urls.py
from django.conf.urls import url, include
from django.urls import path
from api_bit import views

urlpatterns = [
    path('bitCoin/bittest', views.addBitcoin)
]