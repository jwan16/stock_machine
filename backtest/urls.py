from django.conf.urls import url
from django.contrib import admin
from .views import CreateParam, BacktestDetail, UpdateParam, DeleteParam
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
app_name = 'backtest'

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='backtest_detail.html')),
    url(r'^(?P<pk>[0-9]+)$', BacktestDetail.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)$', ModelDetail.as_view(), name='detail'),
    # # url(r'^(?P<pk>[0-9]+)/create_param$', ModelParamCreate.as_view(), name='detail'),
    url(r'^createparam/$', CreateParam),
    url(r'^updateparam/$', UpdateParam),
    url(r'^deleteparam/$', DeleteParam),
    # url(r'^run/$', RunModel)
]
