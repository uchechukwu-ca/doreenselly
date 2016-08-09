# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddInventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to='doreenselly/static/images/document/%Y%m%d', blank=True)),
                ('description', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('shipping_weight', models.DecimalField(max_digits=10, decimal_places=2)),
                ('quantity', models.PositiveIntegerField()),
                ('sold', models.PositiveIntegerField(default=0)),
                ('details', models.CharField(max_length=100)),
                ('category', models.CharField(blank=True, max_length=50, null=True, choices=[('Food', 'Food'), ('Clothing_Product', 'Clothing Product'), ('Leather_Goods', 'Leather Goods'), ('Art_and_Craft', 'Art and Craft')])),
                ('client', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to='doreenselly/static/images/document/%Y%m%d', blank=True)),
                ('description', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('quantity', models.PositiveIntegerField()),
                ('ordered', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_number', models.CharField(max_length=12)),
                ('payable', models.DecimalField(null=True, max_digits=15, decimal_places=2)),
                ('location', models.CharField(max_length=12)),
                ('payment_status', models.CharField(default='Pending', max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')])),
                ('shipment_status', models.CharField(default='Pending', max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped')])),
                ('account_bank_name', models.CharField(max_length=100, null=True, blank=True)),
                ('amount_paid', models.PositiveIntegerField(null=True, blank=True)),
                ('deposit_slip_number', models.PositiveIntegerField(null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.PositiveIntegerField(null=True)),
                ('zipcode', models.PositiveIntegerField(null=True)),
                ('street', models.CharField(max_length=75, null=True)),
                ('country', models.CharField(max_length=32, null=True, choices=[('hide', 'COUNTRY'), ('USA', 'USA'), ('KENYA', 'KENYA')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='order',
            field=models.ForeignKey(blank=True, to='doreenselly.Order', null=True),
        ),
        migrations.AddField(
            model_name='addinventory',
            name='country',
            field=models.ForeignKey(to='doreenselly.Signup', null=True),
        ),
    ]
