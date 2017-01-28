from __future__ import unicode_literals
from django.db.models import Sum
from django.db import models
from django.conf import settings
from datetime import datetime
from collections import OrderedDict

class Employee (models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	hire_date = models.DateField()  #date employee was hired

	def get_full_name(self):
		return self.user.first_name + self.user.last_name

class PayPeriod (models.Model):
	STATUS_UPCOMING = 'upcoming'
    	STATUS_CURRENT = 'current'
    	STATUS_COMPLETE = 'complete'
    	CONTRACT_STATUS = OrderedDict((
		(STATUS_UPCOMING, 'Upcoming'),
		(STATUS_CURRENT, 'Current'),
		(STATUS_COMPLETE, 'Complete'),
	))

	start_date = models.DateTimeField()
	end_date = models.DateTimeField(blank=True, null=True)
	status = models.CharField(choices=CONTRACT_STATUS.items(), default=STATUS_UPCOMING, max_length=32)
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	hourly_rate = models.DecimalField(max_digits = 5, decimal_places = 2)
	#salary = models.DecimalField(max_digits = 8, decimal_places = 2, null = True, blank=True)
	#pay_rate = models.DecimalField(max_digits=5, decimal_places=2)
	total_assigned_hours = models.DecimalField(max_digits = 5, decimal_places = 2),
	
	start_date.currentFilter= True
	
	@property
	def entries(self):
		return Entry.objects.filter( start_time__month = self.start_date.month, start_time__year = self.start_date.year )

	@property
	def total_hours_worked(self): #total billable hours worked
		entries = self.entries
		entries_hours_worked = [entry.hours_worked for entry in entries]
		total_worked = sum(entries_hours_worked)
		return total_worked or 0.0


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
		    ('can_clock_in', 'Can use Pendulum to clock in'),
		    ('can_clock_out', 'Can use Pendulum to clock out'),
#		    ('view_entry_summary', 'Can view entry summary page'),
#		    ('view_payroll_summary', 'Can view payroll summary page'),
#		    ('approve_timesheet', 'Can approve a verified timesheet'),
		)
	
	@property
	def hours_worked(self):
		start = self.start_time
		end = self.end_time
		if not end:
				end = datetime.now()
		delta = end - start
		return delta.days * 24 + delta.seconds / 3600.0

	def check_overlap(self, entry_b, **kwargs):
		"""Return True if the two entries overlap."""
		entry_a = self
		# if entries are open, consider them to be closed right now
		if not entry_a.end_time or not entry_b.end_time:
			return False
		# Check the two entries against each other
		start_inside = entry_a.start_time > entry_b.start_time \
			and entry_a.start_time < entry_b.end_time
		end_inside = entry_a.end_time > entry_b.start_time \
			and entry_a.end_time < entry_b.end_time
		a_is_inside = entry_a.start_time > entry_b.start_time \
			and entry_a.end_time < entry_b.end_time
		b_is_inside = entry_a.start_time < entry_b.start_time \
			and entry_a.end_time > entry_b.end_time
		overlap = start_inside or end_inside or a_is_inside or b_is_inside
			
		return overlap

	def is_overlapping(self):
		if self.start_time and self.end_time:
			entries = self.user.timepiece_entries.filter(
			Q(end_time__range=(self.start_time, self.end_time)) |
			Q(start_time__range=(self.start_time, self.end_time)) |
			Q(start_time__lte=self.start_time, end_time__gte=self.end_time)
			)

			totals = entries.aggregate(max=Max('end_time'), min=Min('start_time'))

			totals['total'] = 0
			for entry in entries:
				totals['total'] = totals['total'] + entry.get_total_seconds()

				totals['diff'] = totals['max'] - totals['min']
				totals['diff'] = totals['diff'].seconds + \
				totals['diff'].days * 86400

				if totals['total'] > totals['diff']:
					return True
				else:
					return False
		else:
			return None

