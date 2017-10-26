from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import FilterDetail, CreateParam, UpdateParam, DeleteParam

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)$', FilterDetail.as_view(), name='filterDetail'),
    url(r'^createparam/$', CreateParam),
    url(r'^updateparam/$', UpdateParam),
    url(r'^deleteparam/$', DeleteParam),
]