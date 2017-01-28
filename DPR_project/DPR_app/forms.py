from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
	username = forms.CharField(label="Username", max_length=30)
	password = forms.CharField(label="Password", max_length=30)

class EmployeeProfileForm(forms.Form):
	email = forms.CharField(label="Email", max_length=30)
	username = forms.CharField(label="Username", max_length=30)
	password = forms.CharField(label="Password", max_length=30)
	last_start_date = forms.DateTimeField(label="Last Start date")
	last_end_date = forms.DateTimeField(label="Last End date")
	hourly_rate = forms.DecimalField(label="Hourly rate")
