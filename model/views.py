# -*- coding: utf-8 -*-
from django.views import generic
from stock.models import Company
import django_tables2 as tables
from django.shortcuts import render, redirect
from django.http import HttpResponse
import operator
from django.db.models import F
from .models import Model, Model_param
from .forms import CreateModelParamForm
from django.contrib.auth.decorators import login_required
from .models import Indicator


class ModelDetail(generic.DetailView):
    model = Model
    template_name = 'model_detail.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ModelDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['param_list'] = Model_param.objects.filter(model_id = self.kwargs.get('pk'))
        return context


class ModelParamCreate(generic.CreateView):
    model = Model_param
    template_name = 'create_param.html'
    fields = ['model', 'indicator', 'param1', 'param2', 'param3']
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

