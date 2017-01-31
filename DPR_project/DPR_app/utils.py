from models import User, Employee, PayPeriod, Entry
from datetime import datetime

def get_active_entry(user):
	entries = Entry.objects.filter(pay_period__employee__user=user, end_time__isnull=True)
	if not entries.exists():
		return None
	return entries

def get_current_pay_period(employee):
	employee_current_pay_period = PayPeriod.objects.filter(employee=employee, end_date__isnull=True, status='current')
	
	now = datetime.now()
	if not employee_current_pay_period:
		return None
		
	employee_current_pay_period = employee_current_pay_period[0]
	if employee_current_pay_period.start_date.month < now.month and employee_current_pay_period.start_date.year < now.year:
		employee_current_pay_period.status = 'Closed'
	return employee_current_pay_period

def get_clocked_in_employees(user):
	today = datetime.now().day
	clocked_in_employees = Employee.objects.filter(clocked_in=True).exclude(user=user)
	return clocked_in_employees
