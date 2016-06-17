"""doreenProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
		https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
		1. Add an import:  from my_app import views
		2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
		1. Add an import:  from other_app.views import Home
		2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
		1. Import the include() function: from django.conf.urls import url, include
		2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from doreenselly import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.views.generic import TemplateView

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', 'doreenselly.views.index', name="index"),
	url(r'^doreenselly/', include('doreenselly.urls')),
	url(r'^delete_item/(?P<item_id>[-\w]+)/$', views.delete_item, name='delete_item'),
	url(r'^admin_delete_item/(?P<item_id>[-\w]+)/$', views.admin_delete_item, name='admin_delete_item'),

	# Password reset urls
	url(r'^reset/form/$', TemplateView.as_view(template_name = 'registration/password_reset_email.html')),
	url(r'^resetpassword/passwordsent/$', password_reset_done, name="password_reset_done"),
	url(r'^reset/password/$', password_reset, name="password_reset"),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name="password_reset_confirm"),
	# url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm',{'post_reset_redirect': '/accounts/password/done/'}, name='password_reset_confirm'),
	url(r'^reset/done/$', password_reset_complete, name="password_reset_complete"),
]


if settings.DEBUG:
 urlpatterns += patterns(
	 'django.views.static',
	 (r'^media/(?P<path>.*)',
	 'serve',
	 {'document_root': settings.MEDIA_ROOT}), )