from django.conf.urls import url

from DPR_app import views

urlpatterns = [
	url(r'^dashboard/$', views.index, name='index'),
	url(r'^pay-period/$', views.pay_period, name='pay-period'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^clock-in/$', views.clock_in, name='clock-in'),
	url(r'^clock-out/$', views.clock_out, name='clock-out'),
	url(r'^export_pay_period_to_csv/$', views.export_pay_period_to_csv, name='export-pay-period-to-csv'),
	url(r'^update-pay-period/(?P<year>\d{4})/(?P<month>\d{1,2})', views.update_pay_period, name='update-pay-period'),
	url(r'^$', views.main, name='main'),
]
