# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import generic
from django.shortcuts import render
from .models import Filter, FilterParam, Parameter
from stock.models import Company, Ratio
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse_lazy
import json
from django.apps import apps

# Create your views here.
def get_filtered_stock_list(param_name, operator, value):
    filter_dict = {
        'current_ratio': Ratio.objects.filter(**{ filter})
    }

class FilterDetail(generic.DetailView):
    model = Filter
    template_name = 'filter.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FilterDetail, self).get_context_data(**kwargs)
        context['param_list'] = FilterParam.objects.filter(filter_id=self.kwargs.get('pk'))
        context['parameters'] = Parameter.objects.all()
        result_list = Company.objects.values_list('stock_id', flat=True).distinct()
        for param in FilterParam.objects.filter(filter_id=self.kwargs.get('pk')):
            try:
                model = apps.get_model(app_label="stock", model_name=param.param_name.data_table)
                model = model.objects.filter(date="2016-12-01")
                filter = param.param_name.attr_name + '__' + param.operator
                result = model.filter(**{ filter: param.value }).values_list('stock_id', flat=True)
                result_list = result_list.intersection(result)
            except: continue
        context['stock_list'] = Company.objects.filter(stock_id__in=result_list)
        return context


def UpdateParam(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    param_values = json.loads(request.POST.get("param_values"))
    param_operators = json.loads(request.POST.get("param_operators"))
    operator_dict = {'>': 'gt', '>=': 'gte', '<': 'lt', '<=': 'lte', '=':'eq'}
    for i in param_operators:
        obj = FilterParam.objects.get(param_id = i)
        obj.operator = operator_dict[param_operators[i]]
        obj.save()
    for i in param_values:
        obj = FilterParam.objects.get(param_id=i)
        obj.value = param_values[i]
        obj.save()
    return HttpResponse('ok')

def CreateParam(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    filter_id = Filter.objects.get(filter_id=request.POST.get("filter_id"))
    param_name = Parameter.objects.get(name = request.POST.get("param_name"))
    FilterParam.objects.create(filter_id=filter_id, param_name=param_name)
    return HttpResponse('ok')

def DeleteParam(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    print(request.POST.get("param_id"))
    obj = FilterParam.objects.get(param_id = request.POST.get("param_id"))
    obj.delete()
    return HttpResponse('ok')
