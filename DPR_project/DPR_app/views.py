from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from models import *
from forms import LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
	template = 'index.html'
	return render(request, template)

def pay_period(request):
	template = 'pay-period.html'

	employee_current_pay_period = Timecard.objects.all();
	context = {
		'items': employee_current_pay_period,
	}

	return render(request, template, context)

def login(request):
	template = 'login.html'
	form = LoginForm
	context = {'form': form}
	return render(request, template, context)

@login_required
def logout(request):
	template = 'logout.html'
	return render(request, template)

@login_required
def main(request):
	template = 'main.html'
	return render(request, template)
