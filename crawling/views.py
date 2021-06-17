#views.py
#-*-coding:utf-8 -*-
from django.http import HttpResponse, JsonResponse
import openpyxl
from .models import Stork
from .models import Bitcoin
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

def addStorks(request):
    filename = 'stork.xlsx'
    book = openpyxl.load_workbook(filename)
    sheet = book.worksheets[0]

    data = []
    for row in sheet.rows:
        data.append([row[0].value, row[1].value])

    length = len(data)

    try:
       for i in range(length-1):
           stork = Stork(stork_id=data[i+1][1], name=data[i+1][0])
           stork.save()

    # 에러에 대한 예외처리는 생략
    except:
        return HttpResponse("ERROR")

    return HttpResponse("Success")

def getStorks(request):
    query = Stork.objects.all()

    data = []

    for i in range(len(query)):
        data.append(query.values()[i])

    return JsonResponse({
        'storks': data
    })

def getStorksByName(request,name):
    query = Stork.objects.filter(name__icontains=name)

    data = []
    for i in range(len(query)):
        data.append(query.values()[i])

    return JsonResponse({
        'storks': data
    })

def getPrice(request, name):

    #쿼리로 가져오는 값은 dictionary 형식
    query = Stork.objects.filter(name=name)
    if len(query.values()) == 0:
        return HttpResponse("Not Found Error")

    data = query.values()[0]

    crawling_id = data['stork_id']

    url = "https://finance.naver.com/item/main.nhn?code=" + crawling_id
    result = requests.get(url)

    bs_obj = BeautifulSoup(result.content, "html.parser")
    no_today = bs_obj.find("p", {"class": "no_today"})
    no_exday = bs_obj.find("p", {"class": "no_exday"})

    price_blind = no_today.find("span", {"class": "blind"})
    variance_blind = no_exday.find("span", {"class": "blind"})

    # 상승 or 하락을 가져오는 소스
    variance_em = no_exday.find("em")
    variance_span = variance_em.find("span")

    now_price = price_blind.text
    variance = variance_blind.text
    variance_sign = variance_span.text

    # json_dumps_params => 한글의 깨짐 방지
    return JsonResponse({
        'price': now_price,
        'variance': variance + "원 " + variance_sign
    }, json_dumps_params={'ensure_ascii': False})

def getSiseUpper(request):
    html = requests.get('https://finance.naver.com/sise/sise_upper.nhn')

    df_kospi_data = []
    df_kosdak_data = []

    table = pd.read_html(html.text)
    df_kospi = table[1]
    df_kospi = df_kospi[['종목명', '연속', '누적', '현재가', '전일비', '거래량', '저가']].dropna()
    # df1 = pd.merge(df1, df_code, how='left', on='종목명')
    if df_kospi.size == 0:
        print("없습니다.")
    else:
        for i in range(len(df_kospi)):
            df_kospi_data.append([df_kospi.loc[i+1][0], df_kospi.loc[i+1][1], df_kospi.loc[i+1][2], df_kospi.loc[i+1][3], df_kospi.loc[i+1][4]])

    df_kosdak = table[2]
    df_kosdak = df_kosdak[['종목명', '연속', '누적', '현재가', '전일비', '거래량', '저가']].dropna()
    # df2 = pd.merge(df2, df_code, how='left', on='종목명')
    if df_kosdak.size == 0:
        print("없습니다.")
    else:
        for i in range(len(df_kosdak)):
            df_kosdak_data.append([df_kosdak.loc[i+1][0], df_kosdak.loc[i+1][1], df_kosdak.loc[i+1][2], df_kosdak.loc[i+1][3], df_kosdak.loc[i+1][4]])

    return JsonResponse({
        'kospi': df_kospi_data,
        'kosdak': df_kosdak_data
    }, json_dumps_params={'ensure_ascii': False})

def getSiseLower(request):
    html = requests.get('https://finance.naver.com/sise/sise_lower.nhn')

    df_kospi_data = []
    df_kosdak_data = []

    table = pd.read_html(html.text)
    df_kospi = table[1]
    df_kospi = df_kospi[['종목명', '연속', '누적', '현재가', '전일비', '거래량', '저가']].dropna()
    # df1 = pd.merge(df1, df_code, how='left', on='종목명')
    if df_kospi.size == 0:
        print("없습니다.")
    else:
        for i in range(len(df_kospi)):
            df_kospi_data.append(
                [df_kospi.loc[i + 1][0], df_kospi.loc[i + 1][1], df_kospi.loc[i + 1][2], df_kospi.loc[i + 1][3],
                 df_kospi.loc[i + 1][4]])

    df_kosdak = table[2]
    df_kosdak = df_kosdak[['종목명', '연속', '누적', '현재가', '전일비', '거래량', '저가']].dropna()
    # df2 = pd.merge(df2, df_code, how='left', on='종목명')
    if df_kosdak.size == 0:
        print("없습니다.")
    else:
        for i in range(len(df_kosdak)):
            df_kosdak_data.append(
                [df_kosdak.loc[i + 1][0], df_kosdak.loc[i + 1][1], df_kosdak.loc[i + 1][2], df_kosdak.loc[i + 1][3],
                 df_kosdak.loc[i + 1][4]])

    return JsonResponse({
        'kospi': df_kospi_data,
        'kosdak': df_kosdak_data
    }, json_dumps_params={'ensure_ascii': False})

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

    return HttpResponse("Success")
