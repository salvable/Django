#views.py
from django.http import HttpResponse
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

def getPrice(request, name):

    #쿼리로 가져오는 값은 dictionary 형식
    query = Stork.objects.filter(name=name)
    data = query.values()[0]

    crawling_id = data['stork_id']

    url = "https://finance.naver.com/item/main.nhn?code=" + crawling_id
    result = requests.get(url)

    bs_obj = BeautifulSoup(result.content, "html.parser")
    no_today = bs_obj.find("p", {"class": "no_today"})
    blind = no_today.find("span", {"class": "blind"})
    print(blind)
    now_price = blind.text

    print(now_price)

    return HttpResponse("Success")