# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-09 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doreenselly', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deposit_slip_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
