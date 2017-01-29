from models import *
from datetime import datetime

def get_active_entry(user): #selectForUpdate
	entries = Entry.objects.filter(pay_period__employee__user=user, end_time__isnull=True)
	#    if select_for_update:
	#        entries = entries.select_for_updat

	if not entries.exists():
		return None
	if entries.count() > 1:
		return 'Only one active entry is allowed.'
	return entries[0]

def get_current_pay_period(employee):
	employee_current_pay_period = PayPeriod.objects.get(employee=employee, end_date__isnull=True)
	if not employee_current_pay_period:
		return None	
	return employee_current_pay_period

#def get_clocked_in_employees():
#	today = datetime.now().day
#	clocked_in_employees = Employee.objects.filter(clocked_in=True)
#	return clocked_in_employees
