# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-26 02:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0006_auto_20171025_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='indicator',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
