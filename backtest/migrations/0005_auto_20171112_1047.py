# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-12 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0004_backtest_capital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backtest_param',
            name='operator',
            field=models.CharField(blank=True, choices=[('>', '>'), ('>=', '>='), ('<', '<'), ('<=', '<='), ('=', '=')], max_length=3, null=True),
        ),
    ]
