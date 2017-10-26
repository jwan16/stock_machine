# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Filter, Parameter, FilterParam
from django.contrib import admin

# Register your models here.
admin.site.register(Filter)
admin.site.register(Parameter)
admin.site.register(FilterParam)