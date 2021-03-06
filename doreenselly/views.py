from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from doreenselly.models import User, Signup, Cart, AddInventory, Order, Blog, ContactUs
from doreenselly.forms import UserForm, SignupForm, AddInventoryForm, BlogForm, ContactUsForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import auth
from .forms import AddInventoryForm

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import random, datetime
from django.utils import timezone
#Imaginary function to handle an upload file

# Create your views here.

def index(request):
	items_from_kenya = AddInventory.objects.filter(country__country="KENYA")
	posts = Blog.objects.all().order_by('-created_on')[0:2]
	print ("POST : ", posts)
	return render(request, "doreenselly/index.html", {'items_from_kenya': items_from_kenya, 'posts': posts })


# def country_signup(request):
# 	return render(request, 'doreenselly/country_signup.html', {})


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
			signup.phone_number = request.POST['phone_number']
			signup.zipcode = request.POST['zipcode']
			signup.street = request.POST['street']
			# signup.city = request.POST['city']
			# signup.state = request.POST['state']
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
				return HttpResponseRedirect('/doreenselly/add_inventory/')
			if user.is_active:
				login(request, user)
				if request.user.signup.country == "KENYA":
					print ("Country ", request.user.signup)
					return HttpResponseRedirect('/doreenselly/homepage/')
				elif request.user.signup.country =="USA":
					print ("Country", request.user.signup)
					return HttpResponseRedirect('https://www.beachbody.com/')
			else:
				return HttpResponse("Your account is disabled.")
		else:
			# return HttpResponseRedirect('/doreenselly/home/')
			print ("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
			# return HttpResponseRedirect('/doreenselly/homepage/')
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
	# items = AddInventory.objects.all()  # Get all items in the database
	print ("YOUR COUNTRY SESSION IS : ", request.user.signup)
	print ("YOUR  NAME IS : ", request.user)
	# if request.user.signup is "KENYA":
	items_from_kenya = AddInventory.objects.filter(country__country="KENYA")
	return render(request, "doreenselly/homepage.html", {'items_from_kenya': items_from_kenya})
	# else:
		# return render(request, 'doreenselly/signin.html', {})
	# items_from_usa = AddInventory.objects.filter(country__country="USA")
	# return render(request, "doreenselly/homepage.html", {'items_from_kenya': items_from_kenya})


@login_required(login_url='/doreenselly/signin/')
def item(request, item_id):    # Client View
	context = {}
	each_item = get_object_or_404(AddInventory, pk=item_id)  # Get item whose item_id matches the primary key in the database
	return render(request, "doreenselly/item.html", {'each_item':each_item})


@login_required()
def cart(request):    # Client View
	request_user = request.user

	items = Cart.objects.filter(client=request_user).filter(ordered=False)
	print ("Items ", items)



	if request.method == "POST":
		print ("rp ", request.POST)
		docfile = request.POST['docfile']
		print ("Docfile", docfile)
		description = request.POST['description']
		print ("Description is ", description)
		price = request.POST['price']
		print ("Price is ", price)
		quantity = request.POST['quantity']
		print ("Quantity is ", quantity)
		client = request.user
		print ("Client is ", client)

		item, created = Cart.objects.get_or_create(client=client, description=description, price=price, quantity=quantity, docfile=docfile)
		item.save()

	# To get the total amount the client is to pay for the item bought
	payable=0
	item=Cart.objects.filter(client=request_user, ordered=False)
	for i in item:
		payable += i.total()
	print ("ANS", payable)

	return render(request, 'doreenselly/cart.html', {'items': items, 'payable': payable})


@login_required()
def delete_item(request, item_id):
	get_item = Cart.objects.get(pk=item_id)
	# print"Id", get_item
	get_item.delete()
	return HttpResponseRedirect('/doreenselly/cart/')


@login_required()
def admin_delete_item(request, item_id):
	get_item = AddInventory.objects.get(pk=item_id)
	# print"Id", get_item
	get_item.delete()
	return HttpResponseRedirect('/doreenselly/add_inventory/')


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
def payment(request):
	context = {}
	request_user = request.user
	item=Cart.objects.filter(client=request_user, ordered=False)
	payable = sum([i.total() for i in item])
	# print "PAYABLE ", payable
	return render(request, "doreenselly/payment.html", {'item': item, 'payable': payable})


def beachbody(request):
	return render(request, "www.beachbody.com", {})


@login_required
def summary1(request, **kwargs):    # Client View
	context = {}
	
	request_user = request.user
	all_items = Cart.objects.filter(client=request_user, ordered=False)
	print ("ALL ITEM", all_items)

	client = request.user
	# print "Client is ", client
	location=request.user.signup.country
	print ("LOCATION ", location)

	if request.method == "POST":
		order_number = create_id()
		print ("ORDER NUMBER", order_number)
		# print "rp ", request.POST
		account_bank_name = request.POST['account_bank_name']
		print ("account_bank_name ", account_bank_name)
		amount_paid = request.POST['amount_paid']
		print ("amount_paid " , amount_paid)
		deposit_slip_number = request.POST['deposit_slip_number']
		print ("deposit_slip_number ", deposit_slip_number)
		payable = request.POST['payable']
		print ("payable ", payable)

		item, created = Order.objects.get_or_create(order_number=order_number, client=client, location=location, account_bank_name=account_bank_name, amount_paid=amount_paid, deposit_slip_number=deposit_slip_number, payable=payable)
		item.save()
		# return redirect('summary')
	

	order = Order.objects.filter(order_number = order_number)
	print ("ORDER", order)
	all_items.update(ordered = True, order = order[0])
	my_order = Order.objects.filter(client=request_user).filter(order_number=order_number) #Populate client's Order to template

	tied_order = Cart.objects.filter(client=request_user, ordered=True, order=order)
	print ("TIED ORDER", tied_order)
	return HttpResponseRedirect(reverse('doreenselly.views.summary'))
	# return render(request, "doreenselly/summary.html", {'my_order': my_order, 'order': order, 'tied_order': tied_order, 'order_number': order_number})


@login_required
def summary(request):
	context = {}
	request_user = request.user
	print ("user", request_user)

	# new_order_num = Order.objects.filter(client=request_user)
	# counting = new_order_num.count()
	# recent_order = new_order_num[counting - 1]
	recent_order = Order.objects.order_by("order_number").last()

	print ("recent_order", recent_order)

	recent_cart_item = Cart.objects.filter(order=recent_order)
	print ("recent_cart_item ",recent_cart_item)

	return render(request, "doreenselly/summary.html", {'recent_order': recent_order, "recent_cart_item": recent_cart_item})


@login_required
def order(request):    # Client View
	context = {}

	request_user = request.user

	order = Order.objects.filter(client=request_user)
	print ("ORDER", order)

	return render(request, "doreenselly/order.html", {'order': order})


@login_required
def add_inventory(request):     #Admin View
	context = {}

	if request.POST:
		print ("REQEST", request.POST)
		add_inventory_form = AddInventoryForm(request.POST, request.FILES)

		if add_inventory_form.is_valid():
			add_inventory = add_inventory_form.save(commit=False)
			# add_inventory.docfile = AddInventory(docfile = request.FILES['docfile'])
			add_inventory.description = request.POST['description']
			add_inventory.price = request.POST['price']
			add_inventory.shipping_weight = request.POST['shipping_weight']
			add_inventory.quantity = request.POST['quantity']
			add_inventory.details = request.POST['details']
			add_inventory.category = request.POST['category']
			add_inventory.client = request.user
			add_inventory.country = request.user.signup
			ans = add_inventory.country
			print("COUNTRY", ans)

			add_inventory.save()

			return HttpResponseRedirect(reverse('doreenselly.views.add_inventory'))
		else:
			print (add_inventory_form.errors)

	else:
		#An empty, unbound form
		add_inventory_form = AddInventoryForm()

	# Load items for the add_inventory page
	all_items = AddInventory.objects.all()


	items_from_kenya = AddInventory.objects.filter(country__country="KENYA")


	return render(request,'doreenselly/add_inventory.html', {'add_inventory_form': add_inventory_form, 'all_items': all_items, 'items_from_kenya': items_from_kenya})


@login_required
def admin_edit_item(request):	      #Admin View
	rp = request.POST
	print ("rp",rp)
	context = {}
	if request.method == "POST":
		product_id = rp.get('item_id')
		print ("product_id", product_id)
		# docfile = rp.get('docfile')
		# print "Docfile is : ", docfile
		description = rp.get('description')
		print ("Description is : ", description)
		price = rp.get('price')
		print ("Price is : ", price)
		quantity = rp.get('quantity')
		print ("Quantity is : ", quantity)
		category = rp.get('category')
		print ("Category is : ", category)

		itemToEdit = get_object_or_404(AddInventory, pk=product_id)
		# print"PK", itemToEdit
		# itemToEdit.docfile = docfile
		itemToEdit.description = description
		itemToEdit.price = price
		itemToEdit.quantity = quantity
		itemToEdit.category = category

		itemToEdit.save()


	return HttpResponseRedirect(reverse('doreenselly.views.add_inventory'))


@login_required
def admin_order_edit(request):	      #Admin View
	rp = request.POST
	print ("rp",rp)
	context = {}
	if request.method == "POST":
		product_id = rp.get('item_id')
		print ("product_id", product_id)
		client = rp.get('client')
		print ("client is : ", client)
		order_number = rp.get('order_number')
		print ("order_number is : ", order_number)
		payable = rp.get('payable')
		print ("payable is : ", payable)
		payment_status = rp.get('pay_status')
		print ("pay_status is : ", payment_status)
		shipment_status = rp.get('ship_status')
		print ("ship_status is : ", shipment_status)

		itemToEdit = get_object_or_404(Order, pk=product_id)
		# print"PK", itemToEdit
		# itemToEdit.client = client
		# itemToEdit.order_number = order_number
		# itemToEdit.payable = payable
		itemToEdit.payment_status = payment_status
		itemToEdit.shipment_status = shipment_status

		itemToEdit.save()


	return HttpResponseRedirect(reverse('doreenselly.views.admin_order_view'))


@login_required
def admin_order_view(request):
	context={}
	
	kenya_order = Order.objects.filter(location="KENYA")
	return render(request, "doreenselly/admin_order_view.html",{'kenya_order': kenya_order})


@login_required
def admin_profile(request):
	return render(request, "doreenselly/admin_profile.html",{})


@login_required
def admin_user_list_view(request):
	context={}
	userlist = User.objects.filter(signup__country="KENYA")
	print "KENYA", userlist
	return render(request, "doreenselly/admin_user_list_view.html",{'userlist': userlist})


def item_search(request):

	if request.method == 'POST':
		print("Got here")
		user_search = request.POST['record']
		print ("What is searched for is : ", user_search)

		category = request.POST['category']
		print ("The category is : ", category)

		if user_search != '' and category =='hide':
			items = AddInventory.objects.filter(Q(description__icontains=user_search)
				)
			# print "items ", items
			return render(request, 'doreenselly/search_result.html', {'items':items, 'user_search_query':user_search})

		if user_search != '' and category != '' :
			items = AddInventory.objects.filter(Q(description__icontains=user_search) , Q(category__icontains=category)
				)
			# print "items", items
			return render(request, 'doreenselly/search_result.html', {'items':items, 'user_search_query':user_search, "category": category})

		if category != '' and user_search =='':
			items = AddInventory.objects.filter(Q(category__icontains=category)
				)
			# print "items ", items
			return render(request, 'doreenselly/search_result.html', {'items':items, 'category':category})

		else:
			return render(request, 'doreenselly/search_result.html', {'error':True})

	else:
		return render(request, 'doreenselly/search_result.html', {'error':True})

	return render(request, 'doreenselly/search_result.html', {'items':items, 'user_search_query':user_search, "category": category})


@login_required
def admin_blog(request):
	context = {}
	if request.POST:
		print ("REQEST", request.POST)
		add_blog_form = BlogForm(request.POST, request.FILES)

		if add_blog_form.is_valid():
			add_blog = add_blog_form.save(commit=False)
			# add_blog.docfile = Addblog(docfile = request.FILES['docfile'])
			add_blog.title = request.POST['title']
			add_blog.body = request.POST['body']

			add_blog.save()

			# items = Addblog.objects.all()
			# print "ITEMS", items

			# return HttpResponse('Success')
			return HttpResponseRedirect(reverse('doreenselly.views.admin_blog'))
		else:
			print (add_blog_form.errors)

	else:
		#An empty, unbound form
		add_blog_form = BlogForm()

	# Load items for the add_blog page
	all_items = Blog.objects.all()


	return render(request,'doreenselly/admin_blog.html', {'add_blog_form': add_blog_form, 'all_items': all_items})


@login_required
def admin_delete_blog(request, item_id):
	get_item = Blog.objects.get(pk=item_id)
	get_item.delete()
	return HttpResponseRedirect('/doreenselly/admin_blog/')


@login_required
def admin_edit_blog(request):
	rp = request.POST
	print ("rp",rp)
	context = {}
	if request.method == "POST":
		product_id = rp.get('item_id')
		print ("product_id", product_id)

		itemToEdit = get_object_or_404(Blog, pk=product_id)
		
		itemToEdit.title = rp.get('title')
		itemToEdit.body = rp.get('body')

		itemToEdit.save()
	return HttpResponseRedirect(reverse('doreenselly.views.admin_blog'))


def blog(request):

	context = {}
	all_items = Blog.objects.all()
	return render(request,'doreenselly/blog.html', {'all_items': all_items})


def contact_us(request):

	context = {}
	if request.POST:
		print ("REQEST", request.POST)
		add_contact_form = ContactUsForm(request.POST, request.FILES)

		if add_contact_form.is_valid():
			add_contact = add_contact_form.save(commit=False)

			add_contact.contact_name = request.POST['contact_name']
			add_contact.contact_email = request.POST['contact_email']
			add_contact.content =  request.POST['content']

			add_contact.save()
			#print('I AM HERE')

			# return HttpResponse('Success')
			return HttpResponseRedirect(reverse('doreenselly.views.contact_us'))
		else:
			print (add_contact_form.errors)

	else:
		#An empty, unbound form
		add_contact_form = ContactUsForm()

	return render(request,'doreenselly/contact_us.html', {'add_contact_form': add_contact_form})


@login_required
def admin_messages(request):

	context = {}
	all_messages = ContactUs.objects.all()
	#print "MESSAGES : ", all_messages
	return render(request,'doreenselly/admin_messages.html', {'all_messages': all_messages})


@login_required
def admin_delete_message(request, item_id):
	get_item = ContactUs.objects.get(pk=item_id)
	# print"Id", get_item
	get_item.delete()
	return HttpResponseRedirect('/doreenselly/admin_messages/')