#views.py
#-*-coding:utf-8 -*-
from django.http import HttpResponse, JsonResponse
from .models import Bitcoin
import requests
import pyupbit
import matplotlib.pyplot as plt


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
    query = Bitcoin.objects.filter(market=code)
    data = []

    for i in range(len(query)):
        data.append(query.values()[i])

    name = data[0]['name']

    url = "https://api.upbit.com/v1/ticker?markets=" + code

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers)

    data = response.json()

    price = data[0]['trade_price']
    high_price = data[0]['high_price']
    low_price = data[0]['low_price']
    change_price = data[0]['change_price']
    change = data[0]['change']

    return JsonResponse({
        'name': name,
        'price': price,
        'highPrice': high_price,
        'lowPrice': low_price,
        'variance': change_price,
        'variance_sign': change
    }, json_dumps_params={'ensure_ascii': False})

def getChart(request, code):
    plt.rcParams["figure.figsize"] = (8, 4)
    plt.rcParams["axes.formatter.limits"] = -10000, 10000

    df = pyupbit.get_ohlcv(code)

    # 가격 차트 그리기
    df = pyupbit.get_ohlcv(code, interval='day', count=100)
    df[["close", "volume"]].plot(secondary_y=["volume"])

    plt.savefig("C:/workSpace/web-react/web-stork/src/Stork/Chart/coinChart.png")

    return JsonResponse({
        'bitcoin': "true"
    }, json_dumps_params={'ensure_ascii': False})