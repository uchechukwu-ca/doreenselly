# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doreenselly', '0005_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='content',
            field=models.TextField(max_length=500),
        ),
    ]
