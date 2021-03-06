# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-11 10:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('model', '0017_auto_20171111_1812'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Backtest',
            fields=[
                ('model_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Backtest_param',
            fields=[
                ('position_type', models.CharField(blank=True, choices=[('buy', 'buy'), ('sell', 'sell')], max_length=10, null=True)),
                ('param_id', models.AutoField(primary_key=True, serialize=False)),
                ('i_param1', models.FloatField(blank=True, null=True)),
                ('i_param2', models.FloatField(blank=True, null=True)),
                ('i_param3', models.FloatField(blank=True, null=True)),
                ('operator', models.CharField(blank=True, choices=[('gt', '>'), ('gte', '>='), ('lt', '<'), ('lte', '<='), ('eq', '=')], max_length=3, null=True)),
                ('eq_diff', models.FloatField(blank=True, null=True)),
                ('param_type', models.CharField(blank=True, choices=[('value', 'value'), ('indicator', 'indicator')], max_length=10, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
                ('ci_param1', models.FloatField(blank=True, null=True)),
                ('ci_param2', models.FloatField(blank=True, null=True)),
                ('ci_param3', models.FloatField(blank=True, null=True)),
                ('backtest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backtest.Backtest')),
                ('compare_indicator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='backtest_i2', to='model.Indicator')),
                ('indicator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='backtest_i1', to='model.Indicator')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('model_param', models.CharField(blank=True, max_length=5000, null=True)),
                ('rundate', models.DateTimeField()),
                ('status', models.CharField(choices=[('running', 'running'), ('done', 'done')], max_length=10)),
                ('result_count', models.IntegerField(blank=True, null=True)),
                ('result_stock_id', models.CharField(blank=True, max_length=10000, null=True)),
                ('backtest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backtest.Backtest')),
            ],
        ),
    ]
