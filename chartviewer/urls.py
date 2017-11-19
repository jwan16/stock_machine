from django.conf.urls import url
from django.contrib import admin
from .views import Chartviewer, Chartviewer_result, StockList
app_name = 'chartviewer'

urlpatterns = [
    url(r'^$', Chartviewer, name='chartviewer'),
    url(r'^results/$', Chartviewer_result),
    url(r'^stocklist/$', StockList)

]
