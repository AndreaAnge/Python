from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from collections import OrderedDict

# Create your models here.

class Employee (models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	email = models.EmailField(max_length = 255, unique = True)
	password = models.CharField(max_length = 50)
	is_active = models.BooleanField(default = True)
	is_admin = models.BooleanField(default = False)
	first_name = models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)

	def get_full_name(self):
		return self.first_name + self.last_name

class Timecard (models.Model):
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	#pay_rate = models.DecimalField(max_digits=5, decimal_places=2)
	
	start_date.currentFilter= True
	def hours_today():
		return self.hours(date.today())

	def pairs(self, day=None):
		p = []
		c = None
		if day:
			stamps = self.stamp_set.filter(stamp_year = day.year, stamp_month = day.month, stamp_day = day.day).order_by('timestamp')
		else:
			stamps = self.stamp_set.order_by('timestamp')

		for stamp in stamps:
			if c == None:
				c = stamp
				continue
			if stamp.timestamp.date() == c.timestamp.date():
				p.insert(0, (c, stamp))
				c = None
			else:
				p.insert(0, (c, None))
				c = stamp
		if c != None:
			p.insert(0, (c, None))

		return p
	
	def hours(self, day=None):
		h = sum([(c.stamp - o.stamp).seconds/ 60./ 60. for o,c in self.pairs(day) if c != None])
		return float("%0.2f" % h)

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

