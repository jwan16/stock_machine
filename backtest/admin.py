from django.contrib import admin

# Register your models here.
from .models import Backtest, Backtest_param, Report
from django.contrib import admin

# Register your models here.
admin.site.register(Backtest)
admin.site.register(Backtest_param)