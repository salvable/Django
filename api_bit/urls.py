# #urls.py
from django.conf.urls import url, include
from django.urls import path
from api_bit import views

urlpatterns = [
    # 코인 종목 api로 불러와 DB에 저장
    # path('bitCoin/bittest', views.addBitcoin),
    # 코인 리스트 불러오기
    path('bitCoin/getBitcoinList', views.getBitcoinList),
    # 코인 리스트 이름으로 불러오기
    path('bitCoin/getBitcoinList/<str:name>', views.getBitcoinListByName),
    # 코인 가격 불러오기
    path('bitCoin/getBitcoinPrice/<str:code>', views.getBitcoinPrice),
    # 차트 그리기
    path('bitCoin/getBitcoinChart/<str:code>', views.getChart),
]