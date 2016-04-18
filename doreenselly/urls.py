from django.conf.urls import patterns, include, url
from doreenselly import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^success/$', views.success, name='success'),
	url(r'^signin/$', views.signin, name='signin'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^home/$', views.home, name='home'),
	url(r'^homepage/$', views.homepage, name='homepage'),
	url(r'^item/(?P<item_id>[-\w]+)/$', views.item, name='item'),
	url(r'^cart/$', views.cart, name='cart'),
	# url(r'^summary/$', views.summary, name='summary'),s
	url(r'^order/$', views.order, name='order'),
	url(r'^add_inventory/$', views.add_inventory, name='add_inventory'),
	url(r'^edit_item/$', views.edit_item, name='edit_item'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)