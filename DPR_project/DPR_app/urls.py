from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^index/', views.index, name='index'),
	url(r'^pay-period/', views.pay_period, name='pay-period'),
	url(r'^profile/', views.profile, name='profile'),
	url(r'^', views.main, name='main'), #must be at the end; redirects all pages to ''
]
