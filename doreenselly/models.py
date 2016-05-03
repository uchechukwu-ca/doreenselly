from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal
# Create your models here.


CATEGORIES = (
	('SELECT', 'SELECT'),
	('USA', 'USA'),
	('KENYA', 'KENYA'),
	)

SHIPMENT_STATUS = (
	('Pending', 'Pending'),
	('Shipped', 'Shipped'),
	)

PAYMENT_STATUS = (
	('Pending', "Pending"),
	('Paid', 'Paid'),
	)


class Signup(models.Model):
	user = models.OneToOneField(User)
	phone_number = models.PositiveIntegerField( null=True)
	zipcode = models.PositiveIntegerField(null=True)
	street = models.CharField(max_length = 75, null=True)
	city = models.CharField(max_length = 75, null=True)
	state = models.CharField(max_length = 75, null= True)
	country = models.CharField(max_length = 32, null=True, choices = CATEGORIES)

	def __str__(self):
		return self.country
		# return "%s - %s" %(self.user.username, self.country)


class AddInventory(models.Model):
	client = models.ForeignKey(User, null=True)
	docfile = models.FileField(upload_to='doreenselly/static/images/document/%Y%m%d', blank=True)
	description = models.CharField(max_length = 100)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	shipping_weight = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField()
	sold = models.PositiveIntegerField(default=0)
	details = models.CharField(max_length = 100)
	country = models.ForeignKey(Signup, null = True)

	def __str__(self):
		return self.country

	def item_remaining(self):
		return self.quantity - self.sold

	def total_payments(self):
		return self.price * self.sold


class Cart(models.Model):
	client = models.ForeignKey(User, null=True)
	docfile = models.FileField(upload_to='doreenselly/static/images/document/%Y%m%d', blank=True)
	description = models.CharField(max_length = 100)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField()
	ordered = models.BooleanField(default=False)
	order = models.ForeignKey('Order', blank=True, null=True)
	created_on = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.description

	def total(self):
		return self.price * self.quantity


class Order(models.Model):
	client = models.ForeignKey(User, null=True)
	order_number = models.CharField(max_length = 12)
	payable = models.DecimalField(max_digits=15, decimal_places=2, null=True)
	location = models.CharField(max_length=12)
	payment_status = models.CharField(max_length=20, choices = PAYMENT_STATUS, default='Pending')
	shipment_status = models.CharField(max_length=20, choices = SHIPMENT_STATUS, default='Pending')
	card_holder_name = models.CharField(max_length = 100)
	card_holder_number = models.PositiveIntegerField()
	card_expiry_month = models.CharField(max_length = 12)
	card_expiry_year = models.PositiveIntegerField()
	created_on = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.order_number