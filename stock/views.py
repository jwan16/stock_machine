# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import urllib
import bs4 as bs
import json
# Return current stock price of:
# DowJones, S&P500, NASDAQ, NYSE, NIKKEI, HSI
def get_indices():
    url = 'https://www.bloomberg.com/markets/stocks'
    html = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(html, 'html5lib')
    table_row = soup.find_all('tr')
    index_list = {'INDU:IND   DOW JONES INDUS. AVG': 'DowJones',
                'SPX:IND   S&P 500 INDEX': 'S&P500',
                'CCMP:IND   NASDAQ COMPOSITE INDEX': 'NASDAQ',
                'NYA:IND   NYSE COMPOSITE INDEX': 'NYSE',
                'NKY:IND   NIKKEI 225': 'NIKKEI',
                'HSI:IND   HANG SENG INDEX': 'HSI',}
    result_list = []
    for tr in table_row:
        td = tr.find_all('td')
        row = [a.text.strip() for a in td]
        if len(row)>0:
            if row[0] in index_list.keys():
                result_list.append({
                    'index': index_list[row[0]],
                    'value': row[1],
                    'net_change': row[2],
                    'change': row[3],
                    '1_month': row[4],
                    '1_year': row[5],
                    'date': row[6],
                })
    return result_list

# Create your views here.
def IndexView(request):
    indices = get_indices()
    print(indices)
    context = {
        'indices': indices,

    }
    return render(request, 'index.html', context)

@login_required
def CreateModel(request):
    model = Model.objects.create(owner = request.user)
    model.save()
    return redirect('/model/'+str(model.model_id))


