# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Model, Model_param, Indicator
from django.contrib import admin

# Register your models here.
admin.site.register(Model)
admin.site.register(Model_param)
admin.site.register(Indicator)