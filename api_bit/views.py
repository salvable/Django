#views.py
#-*-coding:utf-8 -*-
from django.http import HttpResponse, JsonResponse
from .models import Bitcoin
import requests
from django.db import transaction

def addBitcoin(request):
    url = "https://api.upbit.com/v1/market/all"

    querystring = {"isDetails": "false"}

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()

    try:
        for i in range(len(response.json())):
            bitCoin = Bitcoin(market=data[i]['market'], name=data[i]['korean_name'], eng_name=data[i]['english_name'])
            bitCoin.save()

    # 에러에 대한 예외처리는 생략
    except:
        return HttpResponse("ERROR")

    return HttpResponse("success")
