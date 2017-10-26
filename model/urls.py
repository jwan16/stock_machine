from django.conf.urls import url
from django.contrib import admin
from .views import ModelDetail, ModelParamCreate
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
app_name = 'model'

urlpatterns = [
    # /watch/
    url(r'^(?P<pk>[0-9]+)$', ModelDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/create_param$', ModelParamCreate.as_view(), name='detail'),
    url(r'^create/$', login_required(TemplateView.as_view(template_name='model_create.html')))
]
