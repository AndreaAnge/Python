from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'', include('DPR_app.urls')),
    #url(r'^accounts/$', include('django.contrib.auth.urls')),
	url(r'^accounts/login/$', auth_views.login, name='login'),
	url(r'^accounts/logout/$', auth_views.logout_then_login, name='logout')
]
