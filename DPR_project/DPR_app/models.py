from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.conf import settings

from datetime import datetime
from collections import OrderedDict

class Employee (models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	hire_date = models.DateField()
	#line_manager = models.ForeignKey(Employee, blank=True, null=True, related_name='line_manager')
	#is_manager = models.BooleanField(default=False)
	clocked_in = models.BooleanField(default=False)		
	
	def get_full_name(self):
		return self.user.first_name + ' ' + self.user.last_name

class PayPeriod (models.Model):
	STATUS_UPCOMING = 'upcoming'
	STATUS_CURRENT = 'current'
	STATUS_COMPLETE = 'complete'
	PAY_PERIOD_STATUS = OrderedDict((
		(STATUS_UPCOMING, 'Upcoming'),
		(STATUS_CURRENT, 'Current'),
		(STATUS_COMPLETE, 'Complete')
	))

	start_date = models.DateTimeField()
	end_date = models.DateTimeField(blank=True, null=True)
	status = models.CharField(choices=PAY_PERIOD_STATUS.items(), default=STATUS_UPCOMING, max_length=32)
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)
	total_hours_assigned = models.DecimalField(max_digits=5, decimal_places=2, default=160.0)
	
	class Meta:
		ordering = ('-start_date',)
		permissions = (
			('approve_pay_period', 'Can approve a verified timesheet')
		)
	
	@property
	def entries(self):
		return Entry.objects.filter(start_time__month=self.start_date.month, start_time__year=self.start_date.year)

	@property
	def total_minutes_worked(self): #total billable hours worked
		entries = self.entries
		entries_hours_worked = [entry.minutes_worked for entry in entries]
		total_worked = sum(entries_hours_worked)
		return total_worked or 0.0

	def total_worked_formatted(self):
		split_num = str(self.total_minutes_worked).split('.')
		hours = int(split_num[0]) / 60
		minutes = self.total_minutes_worked % 60 
		return '{0}h {1}m'.format(str(hours)[0:2], str(minutes)[0:2])
		
class Entry (models.Model):	
	ENTRY_TYPES = OrderedDict((
		('CLOCK_IN', 'Clock In'),
		('CLOCK_OUT', 'Clock Out')
	))
	
	start_time = models.DateTimeField()
	end_time = models.DateTimeField(blank=True, null=True)   
	#entry_type = models.CharField(max_length=24, choices=ENTRY_TYPES.items())
	pay_period = models.ForeignKey(PayPeriod, on_delete=models.CASCADE)
	
	class Meta:
		ordering = ('-start_time',)
		verbose_name_plural = 'entries'
		permissions = (
		    ('can_clock_in', 'Can use Dashboard to clock in'),
		    ('can_clock_out', 'Can use Dashboard to clock out')
		)
	
	@property
	def minutes_worked(self):
		start = self.start_time
		end = self.end_time
		if not end:
			end = datetime.now()
		delta = end - start	
		return divmod(delta.days * 86400 + delta.seconds, 60)[0]
		
	def delta_formatted(self):
		split_num = str(self.minutes_worked).split('.')
		hours = int(split_num[0][:2]) / 60
		minutes = self.minutes_worked % 60
		return '{0}h {1}m'.format(hours, str(minutes)[0:2])

