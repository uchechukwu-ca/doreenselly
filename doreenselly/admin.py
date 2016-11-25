from django.contrib import admin

from doreenselly.models import Signup, AddInventory, Cart, Order, Blog, ContactUs
# Register your models here.

class SignupAdmin(admin.ModelAdmin):
	list_display = ['phone_number', 'zipcode', 'street', 'country']

admin.site.register(Signup, SignupAdmin)

class AddInventoryAdmin(admin.ModelAdmin):
	list_display = ('client','docfile', 'description', 'price', 'shipping_weight', 'quantity', 'sold', 'item_remaining', 'total_payments', 'details', 'category','country')

admin.site.register(AddInventory, AddInventoryAdmin)

class CartAdmin(admin.ModelAdmin):
	list_display = ('client', 'description', 'price', 'quantity', 'ordered', 'order', 'total', 'created_on')

admin.site.register(Cart, CartAdmin)

class OrderAdmin(admin.ModelAdmin):
	list_display = ('client', 'order_number', 'payable', 'location', 'payment_status', 'shipment_status', 'account_bank_name', 'amount_paid', 'deposit_slip_number', 'created_on')

admin.site.register(Order, OrderAdmin)

class BlogAdmin(admin.ModelAdmin):
	list_display = ('title', 'body', 'logo', 'created_on')

admin.site.register(Blog, BlogAdmin)

class ContactUsAdmin(admin.ModelAdmin):
	list_display = ('contact_name', 'contact_email', 'content')

admin.site.register(ContactUs, ContactUsAdmin)