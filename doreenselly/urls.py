from django.conf.urls import patterns, include, url
from doreenselly import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^signup/$', views.signup, name='signup'),
	# url(r'^country_signup/$', views.country_signup, name='country_signup'),
	url(r'^success/$', views.success, name='success'),
	url(r'^signin/$', views.signin, name='signin'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^homepage/$', views.homepage, name='homepage'),
	url(r'^item/(?P<item_id>[-\w]+)/$', views.item, name='item'),
	url(r'^delete_item/(?P<item_id>[-\w]+)/$', views.delete_item, name='delete_item'),
	# url(r'^admin_delete_item/(?P<item_id>[-\w]+)/$', views.admin_delete_item, name='admin_delete_item'),
	url(r'^cart/$', views.cart, name='cart'),
	url(r'^payment/$', views.payment, name='payment'),
	url(r'^beachbody/$', views.beachbody, name='beachbody'),
	url(r'^summary1/$', views.summary1, name='summary1'),
	url(r'^summary/$', views.summary, name='summary'),
	url(r'^order/$', views.order, name='order'),
	url(r'^add_inventory/$', views.add_inventory, name='add_inventory'),
	# url(r'^itemslist/$', views.itemslist, name='itemslist'),
	url(r'^admin_edit_item/$', views.admin_edit_item, name='admin_edit_item'),
	# url(r'^edit_item/$', views.edit_item, name='edit_item'),
	url(r'^admin_order_view/$', views.admin_order_view, name='admin_order_view'),
	url(r'^admin_order_edit/$', views.admin_order_edit, name='admin_order_edit'),
	url(r'^admin_profile/$', views.admin_profile, name='admin_profile'),
	url(r'^admin_user_list_view/$', views.admin_user_list_view, name='admin_user_list_view'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)