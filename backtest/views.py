from django.views import generic
from stock.models import Company
import django_tables2 as tables
from django.shortcuts import render, redirect
from django.http import HttpResponse
import operator
from django.http import HttpResponse, HttpResponseNotAllowed
from django.db.models import F
from .models import Backtest, Backtest_param, Report
from model.models import Indicator
from django.contrib.auth.decorators import login_required
import os
import json
import datetime
from django.core.mail import send_mail


class BacktestDetail(generic.DetailView):
    model = Backtest

    template_name = 'backtest_detail.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BacktestDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['indicator_list'] = Indicator.objects.all()
        context['trigger_list'] = Backtest_param.objects.filter(backtest_id=self.kwargs.get('pk'), trigger=True)
        context['buy_list'] = Backtest_param.objects.filter(backtest_id = self.kwargs.get('pk'), position_type='buy', trigger=False)
        context['sell_list'] = Backtest_param.objects.filter(backtest_id=self.kwargs.get('pk'), position_type='sell', trigger=False)
        context['report_list'] = Report.objects.filter(backtest_id=self.kwargs.get('pk'))
        return context

def CreateParam(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    backtest_id = Backtest.objects.get(backtest_id=request.POST.get("backtest_id"))
    position = request.POST.get("position")
    Backtest_param.objects.create(backtest = backtest_id, indicator = Indicator.objects.first(), compare_indicator = Indicator.objects.first(), position_type=position)
    send_mail(
        'Create new param',
        'Here is the message.  <br> result:',
        'jasonstockmachine@gmail.com',
        ['wanyichun@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('ok')

def UpdateParam(request):

    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    input = json.loads(request.POST.get("input"))

    for i in input:
        param_id = i['param_id']
        param = Backtest_param.objects.get(param_id = param_id)
        for a in i:
            if i[a]:
                if a == 'indicator' or a == 'compare_indicator':
                    indicator = Indicator.objects.get(name = i[a])
                    setattr(param, a, indicator)
                else:
                    setattr(param, a, i[a])
        param.save()

    date_range = request.POST.get("date_range")
    try:    param.backtest.startdate = datetime.datetime.strptime(date_range[0:10], '%d/%m/%Y')
    except: None
    try:    param.backtest.enddate = datetime.datetime.strptime(date_range[13:], '%d/%m/%Y')
    except: None
    try:    param.backtest.capital = request.POST.get("capital")
    except: None
    param.backtest.save()
    return HttpResponse('ok')

def DeleteParam(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    print(request.POST.get("param_id"))
    obj = Backtest_param.objects.get(param_id = request.POST.get("param_id"))
    obj.delete()
    return HttpResponse('ok')
