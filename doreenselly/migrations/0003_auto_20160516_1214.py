# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-16 11:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doreenselly', '0002_order_deposit_slip_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup',
            name='city',
        ),
        migrations.RemoveField(
            model_name='signup',
            name='state',
        ),
    ]
