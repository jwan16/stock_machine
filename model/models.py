# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from stock.models import Company
# Create your models here.


class Indicator(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, null=True, blank= True)
    param1 = models.CharField(max_length=50, null=True, blank= True)
    param2 = models.CharField(max_length=50, null=True, blank= True)
    param3 = models.CharField(max_length=50, null=True, blank= True)

    def __str__(self):
        return self.name

class Model(models.Model):
    model_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=True, blank= True)
    description = models.CharField(max_length=1000, null=True, blank= True)
    owner = models.ForeignKey(User)
    def __str__(self):
        return self.name

class Model_param(models.Model):
    param_id = models.AutoField(primary_key=True)
    model = models.ForeignKey(Model)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    param1 = models.CharField(max_length=50, null=True, blank= True)
    param2 = models.CharField(max_length=50, null=True, blank= True)
    param3 = models.CharField(max_length=50, null=True, blank= True)


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    model_id = models.ForeignKey(Model)
    RunDate = models.DateTimeField(auto_now=True)
    Status = models.CharField(max_length=10, choices=(('running', 'running'),('done', 'done')))
    result_stock_id = models.CharField(max_length=10000, null=True, blank=True)

class Report_param(models.Model):
    report_id = models.ForeignKey(Report)
    e_name = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    param1 = models.FloatField(max_length=50, null=True, blank=True)
    param2 = models.FloatField(max_length=50, null=True, blank=True)
    param3 = models.FloatField(max_length=50, null=True, blank=True)
