#views.py
from django.http import HttpResponse
import openpyxl
from .models import Stork

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
        print("error")

    return HttpResponse("Success")