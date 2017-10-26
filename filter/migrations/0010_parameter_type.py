# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filter', '0009_auto_20171016_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='type',
            field=models.CharField(choices=[('technical', 'Technical'), ('fundamental', 'Fundamental'), ('ratios', 'Ratios'), ('price', 'Price')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
