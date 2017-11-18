# -*- coding: utf-8 -*-
from django.views import generic
from stock.models import Company
import django_tables2 as tables
from django.shortcuts import render, redirect
from django.http import HttpResponse
import operator
from django.http import HttpResponse, HttpResponseNotAllowed
from django.db.models import F
from .models import Model, Model_param, Indicator, Report
from .forms import CreateModelParamForm
from django.contrib.auth.decorators import login_required
import os
import json




class ModelDetail(generic.DetailView):
    model = Model

    template_name = 'model_detail.html'


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ModelDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['indicator_list'] = Indicator.objects.all()
        context['param_list'] = Model_param.objects.filter(model_id = self.kwargs.get('pk'))
        context['report_list'] = Report.objects.filter(model_id=self.kwargs.get('pk'))
        return context

class ReportDetail(generic.DetailView):
    model = Report
    template_name = 'report_detail.html'

class ModelParamCreate(generic.CreateView):
    model = Model_param
    template_name = 'create_param.html'
    fields = ['model', 'indicator']
    indicator = Indicator.objects.all()
    # success_url = '/model/'


    def get_initial(self):
        return {"model_id": self.kwargs.get("pk")}

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.success_url = '/model/' + self.kwargs.get("pk")
        return super(ModelParamCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ModelParamCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['indicator_list'] = Indicator.objects.all()
        return context

def CreateParam(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    model_id = Model.objects.get(model_id=request.POST.get("model_id"))
    Model_param.objects.create(model = model_id, indicator = Indicator.objects.first(), compare_indicator = Indicator.objects.first())
    return HttpResponse('ok')



def UpdateParam(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    input = json.loads(request.POST.get("input"))
    print(input)
    for i in input:
        param_id = i['param_id']
        param = Model_param.objects.get(param_id = param_id)

        param.indicator = Indicator.objects.get(name = i['indicator'])
        param.compare_indicator = Indicator.objects.get(name = i['compare_indicator'])
        if param.indicator.param3:
            param.i_param1 = i['i_param1']
            param.i_param2 = i['i_param2']
            param.i_param3 = i['i_param3']
        elif param.indicator.param2:
            param.i_param1 = i['i_param1']
            param.i_param2 = i['i_param2']
        else:
            param.i_param1 = i['i_param1']
        param.operator = i['operator']
        if param.operator == '=':
            param.eq_diff = i['eq_diff']
        param.param_type = i['param_type']
        if i['param_type'] == 'indicator':
            if param.compare_indicator.param3:
                param.ci_param1 = i['ci_param1']
                param.ci_param2 = i['ci_param2']
                param.ci_param3 = i['ci_param3']
            elif param.compare_indicator.param2:
                param.ci_param1 = i['ci_param1']
                param.ci_param2 = i['ci_param2']
            else:
                param.ci_param1 = i['ci_param1']
        elif i['param_type'] == 'value':
            param.value = i['value']
        print(param.operator)
        # for a in i:
        #     if i[a]:
        #         if a == 'indicator' or a == 'compare_indicator':
        #             indicator = Indicator.objects.get(name = i[a])
        #             setattr(param, a, indicator)
        #         else:
        #             if i[a]:
        #                 setattr(param, a, i[a])
        param.save()

    return HttpResponse('ok')

def DeleteParam(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    print(request.POST.get("param_id"))
    obj = Model_param.objects.get(param_id = request.POST.get("param_id"))
    obj.delete()
    return HttpResponse('ok')

def RunModel(request):
    model_id = request.POST.get('model_id')
    os.system('python3 manage.py runscript run_model --script-args ' + model_id)
    return HttpResponse('ok')

@login_required
def CreateModel(request):
    model = Model.objects.create(owner = request.user)
    model.save()
    return redirect('/model/'+str(model.model_id))

def UpdateName(request):
    model_id = request.POST.get("model_id")
    name = request.POST.get("name")
    model = Model.objects.get(model_id=model_id)
    model.name = name
    model.save()
    return HttpResponse('ok')