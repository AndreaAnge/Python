from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from collections import OrderedDict

class Employee (models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)

	def get_full_name(self):
		return self.user.first_name + self.user.last_name

class Timecard (models.Model):
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	#pay_rate = models.DecimalField(max_digits=5, decimal_places=2)
	
	start_date.currentFilter= True

class Entry (models.Model):	
	ENTRY_TYPES = OrderedDict((
		('CLOCK_IN', 'Clock In'),
		('CLOCK_OUT', 'Clock Out')
	))

	timestamp = models.DateTimeField()
	entry_type = models.CharField(max_length=24, choices=ENTRY_TYPES.items())
	timecard = models.ForeignKey(Timecard, on_delete=models.CASCADE)
	
	#def check_overlap(self, entry_b, **kwargs):
		#entry_a = self;

#	def is_overlapping(self):

