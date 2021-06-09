#views.py
from django.http import HttpResponse
import pandas as pd


def addStorks(request):
    stork_df = pd.read_csv('stork_List.xls')
    name = stork_df['회사명']
    number = stork_df['종목코드']

    print(name)
    print(number)
    return HttpResponse("Hello, world. Crawling Test." + "number = ")