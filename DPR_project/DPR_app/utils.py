from models import Entry, PayPeriod

def get_active_entry(user): #selectForUpdate
	"""Returns the user's currently-active entry, or None."""
	entries = Entry.objects.filter(user=user, end_time__isnull=True)
	#    if select_for_update:
	#        entries = entries.select_for_updat

	if not entries.exists():
		return None
	if entries.count() > 1:
		raise ActiveEntryError('Only one active entry is allowed.')
	return entries[0]

def get_current_pay_period(employee):
	"""Returns the user's currently-active pay period, or None."""
	employee_current_pay_period = PayPeriod.objects.get(employee=employee, end_date__isnull=True)

	if not employee_current_pay_period:
		return None
		
	return employee_current_pay_period
