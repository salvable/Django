#views.py
#-*-coding:utf-8 -*-
from django.http import HttpResponse, JsonResponse
import openpyxl
from .models import Stork
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from django.db import transaction
from urllib.request import urlopen
import numpy as np
import lxml
import requests
import json
import xmltodict
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt

def addStorks(request):
    filename = 'stork.xlsx'
    book = openpyxl.load_workbook(filename)
    sheet = book.worksheets[0]

    data = []
    for row in sheet.rows:
        data.append([row[0].value, row[1].value])

    length = len(data)

    try:
        sid = transaction.savepoint()

        for i in range(length-1):
           stork = Stork(stork_id=data[i+1][1], name=data[i+1][0])
           stork.save()

    # 에러에 대한 예외처리는 생략
    except:
        # 하나라도 에러가 있다면 rollback
        transaction.savepoint_rollback(sid)
        return HttpResponse("ERROR")

    return HttpResponse("Success")

def getStorks(request):
    query = Stork.objects.all()
    data = []

    if len(query) >= 50:
        for i in range(50):
            data.append(query.values()[i])

    else:
        for i in range(len(query)):
            data.append(query.values()[i])

    return JsonResponse({
        'storks': data
    }, json_dumps_params={'ensure_ascii': False})

def getStorksByName(request,name):
    query = Stork.objects.filter(name__icontains=name)
    data = []

    if len(query) >= 30:
        for i in range(30):
            data.append(query.values()[i])

    else:
        for i in range(len(query)):
            data.append(query.values()[i])

    return JsonResponse({
        'storks': data
    }, json_dumps_params={'ensure_ascii': False})

def getStorkById(request,id):
    query = Stork.objects.filter(stork_id=id)

    # 임시 에러처리
    if len(query) == 0:
        return JsonResponse({
            'error': "404code"
        }, json_dumps_params={'ensure_ascii': False})

    return JsonResponse({
        'storks': query.values()[0]
    }, json_dumps_params={'ensure_ascii': False})

def getPrice(request, id):
    url = "https://finance.naver.com/item/main.nhn?code=" + id
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

    # 고가, 저가 , 거래량, 거래대금
    high = bs_obj.find("em", {"class": "no_up"})
    high_price = high.find("span", {"class": "blind"}).text
    low = bs_obj.find("em", {"class": "no_down"})
    low_price = low.find("span", {"class": "blind"}).text

    # json_dumps_params => 한글의 깨짐 방지
    return JsonResponse({
        'price': now_price,
        'variance': variance + "원 " + variance_sign,
        'highPrice': high_price,
        'lowPrice': low_price
    }, json_dumps_params={'ensure_ascii': False})

def getSiseUpper(request):
    html = requests.get('https://finance.naver.com/sise/sise_upper.nhn')

    df_kospi_data = []
    df_kosdak_data = []

    table = pd.read_html(html.text)
    df_kospi = table[1]
    df_kospi = df_kospi[['종목명', '현재가', '전일비', '등락률']].dropna()
    # df1 = pd.merge(df1, df_code, how='left', on='종목명')
    if df_kospi.size == 0:
        print("없습니다.")
    else:
        for i in range(len(df_kospi)):
            df_kospi_data.append([df_kospi.loc[i+1][0], df_kospi.loc[i+1][1], df_kospi.loc[i+1][2], df_kospi.loc[i+1][3]])

    df_kosdak = table[2]
    df_kosdak = df_kosdak[['종목명', '현재가', '전일비', '등락률']].dropna()
    # df2 = pd.merge(df2, df_code, how='left', on='종목명')
    if df_kosdak.size == 0:
        print("없습니다.")
    else:
        for i in range(len(df_kosdak)):
            df_kosdak_data.append([df_kosdak.loc[i+1][0], df_kosdak.loc[i+1][1], df_kosdak.loc[i+1][2], df_kosdak.loc[i+1][3]])

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
    df_kospi = df_kospi[['종목명', '현재가', '전일비', '등락률']].dropna()
    # df1 = pd.merge(df1, df_code, how='left', on='종목명')
    if df_kospi.size == 0:
        print("없습니다.")
    else:
        for i in range(len(df_kospi)):
            df_kospi_data.append(
                [df_kospi.loc[i + 1][0], df_kospi.loc[i + 1][1], df_kospi.loc[i + 1][2], df_kospi.loc[i + 1][3]])

    df_kosdak = table[2]
    df_kosdak = df_kosdak[['종목명', '현재가', '전일비', '등락률']].dropna()
    # df2 = pd.merge(df2, df_code, how='left', on='종목명')
    if df_kosdak.size == 0:
        print("없습니다.")
    else:
        for i in range(len(df_kosdak)):
            for i in range(len(df_kosdak)):
                df_kosdak_data.append([df_kosdak.loc[i + 1][0], df_kosdak.loc[i + 1][1], df_kosdak.loc[i + 1][2],df_kosdak.loc[i + 1][3]])

    return JsonResponse({
        'kospi': df_kospi_data,
        'kosdak': df_kosdak_data
    }, json_dumps_params={'ensure_ascii': False})

# 상위 거래 5종목 가져오기
def getSiseQuant(request):
    html = requests.get('https://finance.naver.com/sise/sise_quant.nhn')

    df_kospi_data = []

    table = pd.read_html(html.text)
    df_kospi = table[1]
    df_kospi = df_kospi[['종목명', '현재가', '전일비', '등락률']].dropna()

    for i in range(5):
        df_kospi_data.append([df_kospi.loc[i + 1][0], df_kospi.loc[i + 1][1], df_kospi.loc[i + 1][2], df_kospi.loc[i + 1][3]])

    return JsonResponse({
        'kospi': df_kospi_data
    }, json_dumps_params={'ensure_ascii': False})

def getSiseMarket(request):
    html = requests.get('https://finance.naver.com/sise/sise_market_sum.nhn')

    df_kospi_data = []

    table = pd.read_html(html.text)
    df_kospi = table[1]
    df_kospi = df_kospi[['종목명', '현재가', '전일비', '등락률']].dropna()


    for i in range(5):
        df_kospi_data.append([df_kospi.loc[i + 1][0], df_kospi.loc[i + 1][1], df_kospi.loc[i + 1][2], df_kospi.loc[i + 1][3]])


    return JsonResponse({
        'kospi': df_kospi_data
    }, json_dumps_params={'ensure_ascii': False})

def getStorkChart(request, id):

    url = "https://fchart.stock.naver.com/sise.nhn?symbol=" + id + "&timeframe=day&count=200&requestType=0"
    rs = requests.get(url)
    dt = xmltodict.parse(rs.text)
    js = json.dumps(dt)
    js = json.loads(js)

    data = pd.json_normalize(js['protocol']['chartdata']['item'])
    df = data['@data'].str.split('|', expand=True)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    # data handling
    df['Open'] = pd.to_numeric(df['Open'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])
    df['Volume'] = pd.to_numeric(df['Volume'])
    df_final = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df_final_time = pd.DatetimeIndex(df['Date'])
    df_final.index = df_final_time

    # Visualization
    kwargs = dict(type='candle', mav=(5, 20, 60), volume=True)
    mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
    style_final = mpf.make_mpf_style(marketcolors=mc)
    mpf.plot(df_final, **kwargs, style=style_final, savefig="C:/workSpace/web-react/web-stork/src/Stork/Chart/storkChart.png")

    return JsonResponse({
        'storks': "true"
    })