from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from doreenselly.models import User, Signup, Cart, AddInventory, Order
from doreenselly.forms import UserForm, SignupForm, AddInventoryForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import auth
from .forms import AddInventoryForm

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Sum
import random, datetime
#Imaginary function to handle an upload file

# Create your views here.

def index(request):
	return render(request, "doreenselly/index.html",{})


def signup(request):
	context = {}

	if request.method =='POST':
		user_form = UserForm(request.POST)
		signup_form = SignupForm(data=request.POST)

		if user_form.is_valid() and signup_form.is_valid():
			user = user_form.save(commit=False)
			user.set_password(user.password)
			user.save()

			signup = signup_form.save(commit=False)
			signup.user = user
			signup.country = request.POST['country']
			signup.save()
		return HttpResponseRedirect('/doreenselly/success/')
	else:
		context['form'] = UserForm()
		context['signup'] = SignupForm()
	return render(request, "doreenselly/signup.html", context)


def success(request):
	return render(request, "doreenselly/success.html", {})


def signin(request):

	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user:
			if user.is_staff:
				login(request, user)
				return HttpResponseRedirect('/doreenselly/dashboard/')
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/doreenselly/homepage/')
			else:
				return HttpResponse("Your account is disabled.")
		else:
			# return HttpResponseRedirect('/doreenselly/home/')
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'doreenselly/signin.html', {})



def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/doreenselly/')


@login_required()
def dashboard(request):     #Admin View
	context = {}
	return render(request, "doreenselly/dashboard.html", {})


@login_required()
def homepage(request):    # Client View
	context = {}
	items = AddInventory.objects.all()  # Get all items in the database 
	return render(request, "doreenselly/homepage.html", {'items': items})


@login_required()
def item(request, item_id):    # Client View
	context = {}
	each_item = get_object_or_404(AddInventory, pk=item_id)  # Get item whose item_id matches the primary key in the database
	return render(request, "doreenselly/item.html", {'each_item':each_item})


@login_required()
def cart(request):    # Client View
	request_user = request.user

	items = Cart.objects.filter(client=request_user).filter(ordered=False)

	if request.method == "POST":
		print "rp ", request.POST
		docfile = request.POST['docfile']
		print "Docfile", docfile
		description = request.POST['description']
		print "Description is ", description
		price = request.POST['price']
		print "Price is ", price
		quantity = request.POST['quantity']
		print "Quantity is ", quantity
		client = request.user
		print "Client is ", client

		item, created = Cart.objects.get_or_create(client=client, description=description, price=price, quantity=quantity, docfile=docfile)
		item.save()

	return render(request, 'doreenselly/cart.html', {'items': items})


@login_required()
def delete_item(request, item_id):
	get_item = Cart.objects.get(pk=item_id)
	get_item.delete()
	# return HttpResponse("Deleted")
	return HttpResponseRedirect('/doreenselly/cart/')


def LenOf(value):     # Client View
	if len(value) == 2:
		return str(value)
	else:
		return '0' + str(value)


def create_id():    # Client View
	ids = ""
	ids += str(datetime.datetime.today().year)[2:]
	ids += LenOf(str(datetime.datetime.today().month))
	ids += LenOf(str(datetime.datetime.today().second))
	for i in range (0,3):
		ids += str(random.randint(0,9))
	return "D" + ids


@login_required
def summary(request):    # Client View
	# context = {}
	# order_number = create_id()
	# print "ORDER NUMBER", order_number
	request_user = request.user
	all_items = Cart.objects.filter(client=request_user, ordered=False)
	print "ALL ITEM", all_items
	if request.method == "POST":
		# print "rp ", request.POST
		order_number = create_id()
		print "ORDER NUMBER", order_number
		
		client = request.user
		# print "Client is ", client
		location=request.user.signup.country
		print "LOCATION ", location

		item, created = Order.objects.get_or_create(order_number=order_number, client=client, location=location)
		item.save()

		order = Order.objects.filter(order_number = order_number)
		print "ORDER", order
		all_items.update(ordered = True, order = order[0])
		my_order = Order.objects.filter(client=request_user).filter(order_number=order_number) #Populate client's Order to template
	tied_order = Cart.objects.filter(client=request_user, ordered=True, order=order)
	print "TIED ORDER", tied_order
	return render(request, "doreenselly/summary.html", {'my_order': my_order, 'order': order, 'tied_order': tied_order, 'order_number': order_number})


@login_required
def order(request):    # Client View
	context = {}
	# order_number = create_id()
	# print "ORDER NUMBER", order_number
	request_user = request.user
	### all_items = Cart.objects.filter(client=request_user, ordered=False)
	### print "ALL ITEM", all_items
	### if request.method == "POST":
	### 	# print "rp ", request.POST
	### 	order_number = create_id()
	### 	print "ORDER NUMBER", order_number
		
	### 	client = request.user
	### 	# print "Client is ", client
	### 	location=request.user.signup.country
	# 	# print "LOCATION ", location

	### 	item, created = Order.objects.get_or_create(order_number=order_number, client=client, location=location)
	### 	item.save()

	order = Order.objects.filter(client=request_user)
	print "ORDER", order
	### 	all_items.update(ordered = True, order = order[0])
	### 	my_order = Order.objects.filter(client=request_user).filter(order_number=order_number) #Populate client's Order to template
	return render(request, "doreenselly/order.html", {'order': order})


def add_inventory(request):     #Admin View
	context = {}

	if request.POST:
		print "REQEST", request.POST
		add_inventory_form = AddInventoryForm(request.POST, request.FILES)

		if add_inventory_form.is_valid():
			add_inventory = add_inventory_form.save(commit=False)
			# add_inventory.docfile = AddInventory(docfile = request.FILES['docfile'])
			add_inventory.description = request.POST['description']
			add_inventory.price = request.POST['price']
			add_inventory.shipping_weight = request.POST['shipping_weight']
			add_inventory.quantity = request.POST['quantity']
			add_inventory.details = request.POST['details']
			add_inventory.client = request.user

			add_inventory.save()

			items = AddInventory.objects.all()
			print "ITEMS", items

			# return HttpResponse('Success')
			return HttpResponseRedirect(reverse('doreenselly.views.add_inventory'))
		else:
			print add_inventory_form.errors

	else:
		#An empty, unbound form
		add_inventory_form = AddInventoryForm()

	# Load items for the add_inventory page
	items = AddInventory.objects.all()
	print "items",items

	return render(request,'doreenselly/add_inventory.html', {'items': items, 'add_inventory_form': add_inventory_form})




def edit_item(request):	      #Admin View
	rp = request.POST
	print "rp",rp
	context = {}
	if request.method == "POST":
		product_id = rp.get('item_id')
		print "product_id", product_id
		description = rp.get('description')
		print "Description is : ", description
		price = rp.get('price')
		print "Price is : ", price
		quantity = rp.get('quantity')
		print "Quantity is : ", quantity

		itemToEdit = get_object_or_404(AddInventory, pk=product_id)
		print"PK", itemToEdit
		itemToEdit.description = description
		itemToEdit.price = price
		itemToEdit.quantity = quantity

		itemToEdit.save()

		return HttpResponseRedirect('/doreenselly/add_inventory/')
		# return render_to_response('doreenselly/add_inventory.html', {'rp': rp}, context_instance=RequestContext(request))