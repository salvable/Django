#views.py
#-*-coding:utf-8 -*-
from django.http import HttpResponse, JsonResponse
import openpyxl
from .models import Stork
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time

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
    return HttpResponse("SizeUpper")

def getSiseLower(request):
    return HttpResponse("SizeLower")