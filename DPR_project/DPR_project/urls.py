from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth import views
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'DPR_project.views.home', name='home'),
    # url(r'^DPR_project/', include('DPR_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'', include('DPR_app.urls')),
]
