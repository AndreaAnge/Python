from django.conf.urls import url

from DPR_app import views

urlpatterns = [
	url(r'^dashboard/$', views.index, name='index'),
	url(r'^pay-period/$', views.pay_period, name='pay-period'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^clock-in/$', views.clock_in, name='clock-in'),
	url(r'^clock-out/$', views.clock_out, name='clock-out'),
	url(r'^', views.main, name='main'), #must be at the end; redirects all pages to ''
]
