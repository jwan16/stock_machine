# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0023_auto_20171013_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestInfo',
            fields=[
                ('stock_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='stock.Company')),
                ('pe_ratio', models.FloatField(blank=True, null=True)),
                ('market_cap', models.FloatField(blank=True, null=True)),
                ('one_year_change', models.FloatField(blank=True, null=True)),
                ('dividend_yield', models.FloatField(blank=True, null=True)),
                ('average_volume', models.FloatField(blank=True, null=True)),
                ('eps', models.FloatField(blank=True, null=True)),
                ('price_to_sales', models.FloatField(blank=True, null=True)),
                ('price_to_cash_flow', models.FloatField(blank=True, null=True)),
                ('price_to_free_cash_flow', models.FloatField(blank=True, null=True)),
                ('price_to_book', models.FloatField(blank=True, null=True)),
                ('price_to_tangible_book', models.FloatField(blank=True, null=True)),
                ('five_year_eps', models.FloatField(blank=True, null=True)),
                ('five_year_sales_growth', models.FloatField(blank=True, null=True)),
                ('asset_turnover', models.FloatField(blank=True, null=True)),
                ('inventory_turnover', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LatestPriceInfo',
            fields=[
                ('stock_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='stock.Company')),
            ],
        ),
    ]
