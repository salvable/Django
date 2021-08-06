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
    # id로 해당 종목 가져오기
    path('getStorksById/<str:id>', views.getStorkById),
    # 종목 이름으로 크롤링하여 가격 가져오기
    path('stork/<str:id>', views.getPrice),
    # 상한가 크롤링
    path('stork/sise/sise_upper', views.getSiseUpper),
    # 하한가
    path('stork/sise/sise_lower', views.getSiseLower),
    # 거래량 상위
    path('stork/sise/sise_quant', views.getSiseQuant),
    # 시가총액 상위
    path('stork/sise/sise_market', views.getSiseMarket),
    # 특정 주식 그래프 받아오기
    path('stork/getChart/<str:id>', views.getStorkChart)
]