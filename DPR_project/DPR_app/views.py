import datetime
import csv

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseServerError
from django.utils.dates import MONTHS 

from models import *
from utils import * 
from forms import LoginForm, EmployeeProfileForm

@login_required
def main(request):
	template = 'main.html'
	return render(request, template)

@login_required
def index(request):
	template = 'index.html'
	user = request.user
	employee = Employee.objects.get(user=user)
	employee_current_pay_period = get_current_pay_period(employee)
	pay_periods_total_worked = [[pay_period.total_minutes_worked/60] or 0.0 for pay_period in PayPeriod.objects.filter(employee__user__pk=employee.user.pk).order_by('-start_date')[:3]]
	clocked_in_employees = get_clocked_in_employees(user)

	context = {
		'employee_current_pay_period': employee_current_pay_period,
		'disable_clocking': employee_current_pay_period is None,
		'pay_periods_total_worked': pay_periods_total_worked,
		'clocked_in_employees': clocked_in_employees,
		'page_title': 'Dashboard'
	}
	
	return render(request, template, context)

@login_required
def pay_period(request):
	template = 'pay-period.html'
	user = request.user
	employee = Employee.objects.get(user=user)
	employee_current_pay_period = get_current_pay_period(employee)
	
	now = datetime.now()
	months = [{ 'value': datetime(now.year, month, 1).strftime('%B'), 'key': month} for month in MONTHS]
	years = [year for year in range(employee.hire_date.year, now.year + 1)]
	
	context = {
		'months': months,
		'years': years,
		'employee_hire_date': employee.hire_date,
		'employee_current_pay_period': employee_current_pay_period,
		'page_title': 'Pay Period Overview'
	}
	return render(request, template, context)

@login_required
def profile(request):
	template = 'profile.html'
	user = request.user
	employee = Employee.objects.get(user=user)
	
	context = { 'employee': employee, 'page_title': 'Profile'}
	return render(request, template, context)


@login_required
def clock_in(request):
    user = request.user
    active_entry = get_active_entry(user)

    if active_entry:
        message = 'You are already clocked in!'
        return HttpResponseServerError(message)
    else:
		employee = Employee.objects.get(user=user)
		employee_current_pay_period = get_current_pay_period(employee)
		if not employee_current_pay_period:
			return HttpResponseServerError('No active pay periods!')
		entry = Entry(start_time=datetime.now(), pay_period=employee_current_pay_period)
		entry.save()
		employee.clocked_in=True
		employee.save()
		message = 'You have clocked in!'
		
    return HttpResponse(message)

@login_required
def clock_out(request):
    active_entry = get_active_entry(request.user)

    if not active_entry:
		message = 'Not clocked in'
		return HttpResponseServerError(message)
    elif active_entry.count() > 1:
		message = 'Only one active entry is allowed. Please contact your manager.'
		return HttpResponseServerError(message)
    else:
		active_entry = active_entry.first()
		active_entry.end_time = datetime.now()
		active_entry.save()
		message = 'You have clocked out!'
		
    return HttpResponse(message)


@login_required
def export_pay_period_to_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
	
	user = request.user
	employee = Employee.objects.filter(user=user)
	employee_current_pay_period = get_current_pay_period(employee)
	entries = employee_current_pay_period.entries
	writer = csv.writer(response)
	
	for entry in entries:
		writer.writerow([entry.start_time.date(), entry.start_time, entry.end_time, entry.delta_formatted()])
		
	return response

def update_pay_period(request, year, month):
	year_selected = year
	month_selected = month
	
	user = request.user
	employee = Employee.objects.get(user=user)
	employee_pay_period = PayPeriod.objects.filter(employee=employee, start_date__month=month, start_date__year=year_selected)
	
	if employee_pay_period:
		employee_pay_period = employee_pay_period.first()
		
	return render(request, 'pay_period_table.html', {'employee_current_pay_period': employee_pay_period})

#def lock_pay_period(request):
	#user = request.user
	#employee = Employee.objects.filter(user=user)
	#employee_current_pay_period = get_current_pay_period(employee)
	#employee_current_pay_period.status = 
	
