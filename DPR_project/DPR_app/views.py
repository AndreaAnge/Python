import datetime
from django.shortcuts import render_to_response
from django.shortcuts import render, redirect
from django.template import loader
from models import *
from forms import LoginForm, EmployeeProfileForm
from django.contrib.auth.decorators import login_required, permission_required
from utils import * 
from django.http import HttpResponse

@login_required
def main(request):
	template = 'main.html'
	return render(request, template)

@login_required
def index(request):
	template = 'index.html'
	pay_periods_total_worked = [[pay_period.total_hours_worked] for pay_period in PayPeriod.objects.all().order_by('-id')[:3]]
#	clocked_in_employees = get_clocked_in_employees()
	context = { 
		'pay_periods_total_worked': pay_periods_total_worked,
		'page_title': 'Dashboard'
	}
	return render(request, template, context)

@login_required
def pay_period(request):
	template = 'pay-period.html'
	user = request.user
	employee = Employee.objects.filter(user = user)
	employee_current_pay_period = get_current_pay_period(employee)
	context = {
		'employee_current_pay_period': employee_current_pay_period,
		'page_title': 'Pay Period Overview'
	}
	return render(request, template, context)

@login_required
def profile(request):
	template = 'profile.html'
	form = EmployeeProfileForm()
	context = { 'form': form }
	return render(request, template, context)
	
def clock_in(request):
    user = request.user
    active_entry = get_active_entry(user)
    if active_entry:
        message = 'You are already clocked in!'
    else:
		employee = Employee.objects.filter(user = user)
		employee_current_pay_period = get_current_pay_period(employee)
		entry = Entry(start_time=datetime.now())
		entry.save()
		employee_current_pay_period.entries.add(entry)
		message = 'You have clocked in!'
    return HttpResponse(message)

def clock_out(request):
    entry = get_active_entry(request.user)
    if not entry:
		message = "Not clocked in"
    else:
		entry.end_time = datetime.now()
		entry.save()
		message = 'You have clocked out!.'
    return HttpResponse(message)
