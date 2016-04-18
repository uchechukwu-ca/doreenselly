# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-15 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doreenselly', '0004_order_docfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='docfile',
        ),
        migrations.AddField(
            model_name='cart',
            name='docfile',
            field=models.FileField(blank=True, upload_to='doreenselly/static/images/document/%Y%m%d'),
        ),
    ]
