#views.py
#-*-coding:utf-8 -*-
from django.http import HttpResponse, JsonResponse
from .models import Bitcoin
import requests
from django.db import transaction
import pyupbit


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


def getBitcoinList(request):
    query = Bitcoin.objects.all()
    data = []

    for i in range(len(query)):
        data.append(query.values()[i])

    return JsonResponse({
        'bitcoin': data
    }, json_dumps_params={'ensure_ascii': False})


def getBitcoinListByName(request, name):
    query = Bitcoin.objects.filter(name__icontains=name)
    data = []

    for i in range(len(query)):
        data.append(query.values()[i])

    return JsonResponse({
        'bitcoin': data
    }, json_dumps_params={'ensure_ascii': False})

def getBitcoinPrice(request, code):
    url = "https://api.upbit.com/v1/ticker?markets=" + code

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers)

    data = response.json()

    print(data[0])
    print(data[0]['market'])

    price = data[0]['trade_price']
    high_price = data[0]['high_price']
    low_price = data[0]['low_price']
    change_price = data[0]['change_price']
    change = data[0]['change']

    return JsonResponse({
        'price': price,
        'high_price': high_price,
        'low_price': low_price,
        'change_price': change_price,
        'change': change
    }, json_dumps_params={'ensure_ascii': False})
