# https://cholol.tistory.com/468?category=739855 참고


# #urls.py
from django.conf.urls import url, include
from django.urls import path
from crawling import views

urlpatterns = [
    # addStorks는 DB에 .xlsx 정보를 가져오기위해 최초 한번만 실행할 것, 실행 후에는 주석처리
    # path('addStorks/', views.addStorks),
    # 목록들 가져오기
    path('getStorks/', views.getStorks),
    # 이름으로 해당되는 목록들 가져오기
    path('getStorks/<str:name>', views.getStorksByName),
    # 종목 이름으로 크롤링하여 가격 가져오기
    path('stork/<str:name>', views.getPrice),
    # 상한가 크롤링
    path('stork/sise/sise_upper', views.getSiseUpper),
    # 하한가 크롤링
    path('stork/sise/sise_lower', views.getSiseLower),
]