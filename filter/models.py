# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from stock.models import Company, Ratio

# Create your models here.
class Parameter(models.Model):
    PARAM_TYPE = (('technical', 'Technical'),('fundamental', 'Fundamental'), ('ratios', 'Ratios'), ('price', 'Price'))
    TABLE_NAME = (('RATIO', 'RATIO'), ('TECHNICAL', 'TECHNICAL'))
    name = models.CharField(max_length=30, primary_key=True)
    attr_name = models.CharField(max_length=30)
    data_table = models.CharField(max_length=50, choices = TABLE_NAME)
    type = models.CharField(max_length=20, choices = PARAM_TYPE)

    def __str__(self):
        return str(self.name)

class Filter(models.Model):
    filter_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User)
    def __str__(self):
        return str(self.name)

class FilterParam(models.Model):
    OPERATOR_CHOICES = (('gt', '>'), ('gte', '>='), ('lt', '<'), ('lte','<='), ('eq', '='))
    param_name = models.ForeignKey(Parameter)
    filter_id = models.ForeignKey(Filter)
    param_id = models.AutoField(primary_key=True)
    operator = models.CharField(max_length=3, choices=OPERATOR_CHOICES, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    def __str__(self):
        return str(self.param_id)