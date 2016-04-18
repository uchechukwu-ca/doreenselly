from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from doreenselly.models import CATEGORIES, Signup, AddInventory


class UserForm(forms.ModelForm):
	firstname = forms.CharField(max_length=32, required=True, help_text="Firstname")
	username = forms.CharField(max_length=32, required=True, help_text="Username")
	email = forms.EmailField(max_length=32, required=True, help_text="Email")
	password = forms.CharField(required=True, widget=forms.PasswordInput(), help_text="Password")

	class Meta:
		model = User
		fields = ('firstname', 'username', 'email', 'password')


class SignupForm(forms.ModelForm):
	country = forms.ChoiceField(choices=CATEGORIES, widget=forms.Select(choices= CATEGORIES), required = True)

	class Meta:
		model = Signup
		fields = ('country',)

class AddInventoryForm(forms.ModelForm):
	docfile = forms.FileField( help_text='max. 42 megabytes', required = True)
	description = forms.CharField( required = True)
	price = forms.DecimalField(max_digits=10, decimal_places=2, required = True)
	shipping_weight = forms.DecimalField(max_digits=10, decimal_places=2, required = True)
	quantity = forms.IntegerField(required = True)
	details = forms.CharField(widget=forms.Textarea, required = True)

	class Meta:
		model = AddInventory
		fields = ('docfile', 'description', 'price', 'shipping_weight', 'quantity', 'details')