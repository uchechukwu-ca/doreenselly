from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from doreenselly.models import CATEGORIES, Signup, AddInventory


class UserForm(forms.ModelForm):
	firstname = forms.CharField(help_text="First Name", required = True,widget=forms.TextInput(attrs={'class':'form-control', 'class':'form-control', 'placeholder':'First Name', 'required':'required'}))
	lastname = forms.CharField(help_text="Last Name", required = True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name', 'required':'required'}))
	username = forms.CharField(help_text="Username", required = True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usernme', 'required':'required'}))
	email = forms.EmailField(help_text="E-Mail", required = True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'E-Mail', 'required':'required'}))
	password = forms.CharField(help_text="Password", required = True, max_length=15, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password','required':'required'}))

	class Meta:
		model = User
		fields = ('firstname', 'lastname', 'username', 'email', 'password')


class SignupForm(forms.ModelForm):
	phone_number = forms.IntegerField(help_text = "Phone Number",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone Number', 'required':'required', 'id':'phone_number'}))
	zipcode = forms.IntegerField(help_text = "Zipcode",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Zipcode', 'required':'required','id':'zip_code'}))
	street = forms.CharField(help_text = "Street", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Street Name/Number', 'required':'required'}))
	city = forms.CharField(help_text = "City", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City', 'required':'required'}))
	state = forms.CharField(help_text = "State", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State', 'required':'required'}))
	country = forms.ChoiceField(choices=CATEGORIES, widget=forms.Select(attrs={'class':'form-control', 'required':'required'}), required = True)

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