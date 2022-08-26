from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django.contrib.auth import authenticate
from django.http import HttpResponse

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		model = Account
		fields = ('email', 'username','fname','lname','bike_no','contact_no', 'password1', 'password2', )

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email'].lower()
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use' %email)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username'].lower()
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use'% account.username)


	def clean_bike_no(self):
		if self.is_valid():
			bike_no = self.cleaned_data['bike_no']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(bike_no=bike_no)
			except Account.DoesNotExist:
				return bike_no
			raise forms.ValidationError('Bike  "%s" is already registered'% account.bike_no)

	def clean_contact_no(self):
		if self.is_valid():
			contact_no = self.cleaned_data['contact_no']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(contact_no=contact_no)
			except Account.DoesNotExist:
				return contact_no
			raise forms.ValidationError('Number "%s" is already in use'% account.contact_no)


class AccountAuthenticaticationForm(forms.ModelForm):
	password    = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model   = Account
		fields  = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email       = self.cleaned_data['email']
			password    = self.cleaned_data['password']

			if not authenticate(email=email, password=password):
				try:
					account = Account.objects.get(email=email)
				except Account.DoesNotExist:
					return HttpResponse(email)
				raise forms.ValidationError("Account Does Not Exists")

class AccountUpdateForm(forms.ModelForm):
	class Meta:
		model   = Account
		fields  = ('email', 'username', 'fname', 'lname', 'bike_no', 'contact_no')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email'].lower()
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use' %email)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username'].lower()
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use'% account.username)


	def clean_bike_no(self):
		if self.is_valid():
			bike_no = self.cleaned_data['bike_no']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(bike_no=bike_no)
			except Account.DoesNotExist:
				return bike_no
			raise forms.ValidationError('Bike  "%s" is already registered'% account.bike_no)

	def clean_contact_no(self):
		if self.is_valid():
			contact_no = self.cleaned_data['contact_no']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(contact_no=contact_no)
			except Account.DoesNotExist:
				return contact_no
			raise forms.ValidationError('Number "%s" is already in use'% account.contact_no)




