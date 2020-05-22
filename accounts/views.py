from django.shortcuts import render, redirect
from django import forms
from .models import *
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm as RF, AccountAuthenticaticationForm as AAF, AccountUpdateForm as UF
from django.contrib import messages
#from another tutorial
from django.contrib.auth.models import User


def registration_view(request):
	context = {}
	form = RF()
	if request.method == 'POST':
		form = RF(request.POST)
		if form.is_valid():
			form.save()
			email           = form.cleaned_data.get('email')
			raw_password    = form.cleaned_data.get('password1')
			username        = form.cleaned_data.get('username')
			bike_no         = form.cleaned_data.get('bike_no')
			contact_no      = form.cleaned_data.get('contact_no')
			account         = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('soc:home')
		else:
			print(form)
			context['rf'] = form
	else:
		form    = RF()
		context['rf'] = form
	return render(request, 'accounts/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('soc:home')

def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("soc:home")

	if request.POST:
		form = AAF(request.POST)
		if form.is_valid():
			email    = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user is not None:
				login(request, user)
				return redirect('soc:home')
		else:
			messages.info(request,'Invalid Credentials')
			print(form)
			return redirect('login')
	else:
		form = AAF()

	context['login_form'] = form
	# messages.info(request,'Invalid Credentials')
	return render(request, "accounts/login.html", context)


def account_view(request):
	if not request.user.is_authenticated:
		return redirect("login")

	context = {}

	if request.POST:
		form = UF(request.POST, instance=request.user)

		if form.is_valid():
			form.save()
	else:
		form = UF(
				initial={
					"email"               :  request.user.email,
					"fname"               :  request.user.fname,
					"lname"               :  request.user.lname,
					"username"            :  request.user.username,
					"bike_no"             :  request.user.bike_no,
					"contact_no"          :  request.user.contact_no,
				}
		)
	context['uf'] = form
	return render(request, 'update.html', context)


#https://medium.com/@renjithsraj/how-to-reset-password-in-django-bd5e1d6ed652

# def registration_view(request):
#     context = {}
#     form = RF()
#     if request.POST:
#         form = RF(request.POST)
#         if form.is_valid():
#             form.save()
#             email   = forms.clean_data.get('email')
#             # email   = forms.clean_data.get('email')
#             # email   = forms.clean_data.get('email')
#             # email   = forms.clean_data.get('email')

#             # raw_password = form.cleaned_data.get('password1')
#             # account      = authenticate(email=email, password=raw_password)
#             # login(request, account)
#             # print("1")
#             return redirect('main:home')
#         else:
#             context['rf'] = form
#     else:
#         form    = RF()
#         context['rf'] = form
#     print("2")
#     return render(request, 'accounts/register.html', context)

# def registration_view(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('main:home')
#     else:
#         form = RegistrationForm()

#         args = {'form':form}
#         return render(request, 'accounts/register.html',args)




#1st
# def registration_view(request):
#     context = {}
#     if request.method == 'POST':
#         email               =  request.POST['email']
#         fname               =  request.POST['faname']
#         lname               =  request.POST['lname']
#         username            =  request.POST['username']
#         bike_no             =  request.POST['bike_no']
#         contact_no          =  request.POST['contact_no']
#         password1           =  request.POST['password1']
#         password2           =  request.POST['password2']

#     # account         =  Account(username=username, password= password1, email=email, **extra_fields)
#     account         =  Account(email=email, fname=fname, lname=lname, username=username, bike_no=bike_no, contact_no=contact_no, password1=password1, password2=password2 )
#     # user = User.objects.create_user(username=username, password= password1, email=email, **extra_fields)
#     if account.is_valid()





#from previous