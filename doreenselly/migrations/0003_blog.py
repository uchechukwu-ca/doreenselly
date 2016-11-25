# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doreenselly', '0002_auto_20160809_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Blog Title')),
                ('body', models.TextField(max_length=500, verbose_name='Enter the details of the blog')),
                ('logo', models.ImageField(upload_to='blogsImage', verbose_name='Please add the Image or Logo of the blog')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
