# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-13 15:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0002_indicator_creationdate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indicator',
            old_name='creationDate',
            new_name='dateCreated',
        ),
    ]
