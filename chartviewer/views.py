# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from stock.models import Company
import json
# Create your views here.

def add_zero(stock_id):
    if len(stock_id) < 2:
        stock_id = '000' + str(stock_id)
    elif len(stock_id) < 3:
        stock_id = '00' + str(stock_id)
    elif len(stock_id) < 4:
        stock_id = '0' + str(stock_id)
    else:
        stock_id = str(stock_id)
    return stock_id


def Chartviewer(request):
    return render(request, 'chartviewer.html')
def Chartviewer_result(request):
    if not request.is_ajax() or not request.method=='POST':
        return render(request, 'chartviewer.html')
    input = request.POST.get("input")
    period = json.loads(request.POST.get("period"))
    print(period)
    stock_list = input.split(',')
    param = {'fontsize': 12,
            '15MinDelay': 'N',
            'lang': 1,
            'titlestyle': 1,
            'vol': 1,
            'Indicator': 1,
            'indpara1': 10,
            'indpara2': 20,
            'indpara3': 50,
            'indpara4': 100,
            'indpara5': 150,
            'subChart1': 2,
            'ref1para1': 14,
            'ref1para2': 0,
            'ref1para3': 0,
            'subChart2': 3,
            'ref2para1': 12,
            'ref2para2': 26,
            'ref2para3': 9,
            'subChart3': 7,
            'ref3para1': 14,
            'ref3para2': 3,
            'ref3para3': 0,
            'scheme': 1,
            'com': 100,
            'chartwidth': 673,
            'chartheight': 820,
            'type': 1,
            'logoStyle': 1,
             }
    result_list = []
    base_url = 'http://charts.aastocks.com/servlet/Charts?'
    for stock_id in stock_list:
        url_list = []
        result = {}
        param['stockid'] = str(stock_id) + '.hk'
        url = base_url
        for i in param:
            url = url + str(i) + '=' + str(param[i]) + '&'
        for a in period:
            url_list.append(url + 'period=' + str(a) + '&')
        result['id'] = add_zero(stock_id) + '.hk'
        try:
            result['name'] = Company.objects.get(stock_id=add_zero(stock_id)).name
        except:
            result['name'] = ''
        result['url'] = url_list
        result_list.append(result)
    context = {
        'result_list': result_list,
    }
    return render(request, 'chartviewer_result.html', context)

def StockList(request):
    json_file = open('chartviewer/stock_list.json')
    stock_list = json.load(json_file)
    stockgroup = request.POST.get('stockgroup')
    print(stockgroup)
    stocks = stock_list[stockgroup]
    result_list = []
    for stock in stocks:
        result = {}
        result['stock_id'] = stock
        result['name'] = stocks[stock]
        result_list.append(result)
    context = {
        'stocks': result_list
    }
    return render(request, "stock_list.html", context)