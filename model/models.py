# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from stock.models import Company
# Create your models here.


class Indicator(models.Model):
    name = models.CharField(max_length=50)
    function = models.CharField(max_length=100)
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
        return str(self.model_id)

class Model_param(models.Model):
    OPERATOR_CHOICES = (('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<='), ('=', '='))
    param_id = models.AutoField(primary_key=True)
    model = models.ForeignKey(Model, null=True, blank=True)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, null=True, blank=True)
    i_param1 = models.FloatField(null=True, blank=True)
    i_param2 = models.FloatField(null=True, blank=True)
    i_param3 = models.FloatField(null=True, blank=True)
    operator = models.CharField(max_length=3, choices=OPERATOR_CHOICES, null=True, blank=True)
    eq_diff = models.FloatField(null=True, blank=True)
    param_type = models.CharField(max_length=10, choices=(('value', 'value'),('indicator', 'indicator')),null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    compare_indicator = models.ForeignKey(Indicator, null=True, blank=True, related_name='compare')
    ci_param1 = models.FloatField(null=True, blank=True)
    ci_param2 = models.FloatField(null=True, blank=True)
    ci_param3 = models.FloatField(null=True, blank=True)



class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    model = models.ForeignKey(Model)
    model_param = models.CharField(max_length=5000, null=True, blank=True)
    rundate = models.DateTimeField()
    status = models.CharField(max_length=10, choices=(('running', 'running'),('done', 'done')))
    result_count = models.IntegerField(null=True, blank=True)
    result_stock_id = models.CharField(max_length=10000, null=True, blank=True)
    def __str__(self):
        return str(self.report_id)

