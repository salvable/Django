# https://cholol.tistory.com/468?category=739855 참고


# #urls.py
from django.conf.urls import url, include
from django.urls import path
from crawling import views

urlpatterns = [
    # addStorks는 DB에 .xlsx 정보를 가져오기위해 최초 한번만 실행할 것
    path('addStorks/', views.addStorks),
    path('stork/<str:name>', views.getStork)
]