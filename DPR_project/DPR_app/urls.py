from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^index/', views.index, name='index'),
	url(r'^pay-period/', views.pay_period, name='pay-period'),
	url(r'^', views.main, name='main'),
	#url(r'^login/', views.login, name='login'),
]
