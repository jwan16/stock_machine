from django.conf.urls import url
from django.contrib import admin
from .views import ModelDetail, CreateParam, UpdateParam, DeleteParam, RunModel, ReportDetail, CreateModel, UpdateName
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
app_name = 'model'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)$', ModelDetail.as_view(), name='detail'),
    url(r'^report/(?P<pk>[0-9]+)$', ReportDetail.as_view(), name='report_detail'),
    # url(r'^(?P<pk>[0-9]+)/create_param$', ModelParamCreate.as_view(), name='detail'),

    # Model
    url(r'^create/$', CreateModel),
    url(r'^updatename/$', UpdateName),

    # Model param
    url(r'^createparam/$', CreateParam),
    url(r'^updateparam/$', UpdateParam),
    url(r'^deleteparam/$', DeleteParam),
    url(r'^run/$', RunModel)

]
