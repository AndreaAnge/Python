from django.conf.urls import *

from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/logout/', 'django.contrib.auth.views.logout'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
	url(r'', include('DPR_app.urls')),
]
