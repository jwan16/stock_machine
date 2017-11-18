from django.conf.urls import url
from django.contrib import admin
from .views import IndexView

app_name = 'stock'

urlpatterns = [
    url('^$', IndexView, name='index')
]
