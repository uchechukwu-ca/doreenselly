# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doreenselly', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addinventory',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[('Food', 'Food'), ('Clothing_Products', 'Clothing Products'), ('Leather_Goods', 'Leather Goods'), ('Art_and_Craft', 'Art and Craft')]),
        ),
    ]
