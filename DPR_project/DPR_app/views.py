import datetime
from django.shortcuts import render_to_response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from models import *
from forms import LoginForm, EmployeeProfileForm
from django.contrib.auth.decorators import login_required, permission_required
from utils import * 

@login_required
def main(request):
	template = 'main.html'
	return render(request, template)

@login_required
def index(request):
	template = 'index.html'
	return render(request, template)

@login_required
def pay_period(request):
	template = 'pay-period.html'
	user = request.user
	employee = Employee.objects.filter(user = user)
	employee_current_pay_period = get_current_pay_period(employee)
	context = {
		'employee_current_pay_period': employee_current_pay_period,
	}
	print(employee_current_pay_period.entries)
	return render(request, template, context)

@login_required
def profile(request):
	template = 'profile.html'
	form = EmployeeProfileForm()
	context = { 'form': form }
	return render(request, template, context)
	
@permission_required('entries.can_clock_in')
def clock_in(request):
    """For clocking the user into a project."""
    user = request.user
    # Lock the active entry for the duration of this transaction, to prevent
    # creating multiple active entries.
    active_entry = get_active_entry(user, select_for_update=True)

    initial = dict([(k, v) for k, v in request.GET.items()])
    data = request.POST or None
    form = ClockInForm(data, initial=initial, user=user, active=active_entry)
    if form.is_valid():
        entry = form.save()
        message = 'You have clocked into {0} on {1}.'.format(
            entry.activity.name, entry.project)
        messages.info(request, message)
        return HttpResponseRedirect(reverse('dashboard'))

    return render(request, 'timepiece/entry/clock_in.html', {
        'form': form,
        'active': active_entry,
    })


@permission_required('entries.can_clock_out')
def clock_out(request):
    entry = utils.get_active_entry(request.user)
    if not entry:
        message = "Not clocked in"
        messages.info(request, message)
        return HttpResponseRedirect(reverse('dashboard'))
    if request.POST:
        form = ClockOutForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            message = 'You have clocked out of {0} on {1}.'.format(
                entry.activity.name, entry.project)
            messages.info(request, message)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            message = 'Please correct the errors below.'
            messages.error(request, message)
    else:
        form = ClockOutForm(instance=entry)
    return render(request, 'timepiece/entry/clock_out.html', {
        'form': form,
        'entry': entry,
})
