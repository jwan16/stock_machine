# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_auto_20170603_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratio',
            name='RAT_Year',
            field=models.DateField(),
        ),
    ]
