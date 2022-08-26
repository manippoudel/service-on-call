from django.views.generic import TemplateView
from .models import (
	about_member,
	home_page,
	Service_Provider,
	Review,
)
from django.shortcuts import get_object_or_404, render,redirect
from .forms import *
from django.db.models import Avg
from accounts.models import  Account




class home_view(TemplateView):
	template_name = "soc/index.html"

	def get_context_data(self, **kwargs):
		context         = super(home_view, self).get_context_data(**kwargs)
		context['sps']   = Service_Provider.objects.filter(is_approved=True)
		context['hps']   = home_page.objects.all()
		context['ams']   = about_member.objects.all()
		context['reviews'] = Review.objects.all()
		return context

def list_sp(request):
	context = {}
	allsp = Service_Provider.objects.filter(is_approved=True)
	context = {
		"sp": allsp, 
	}
	return render(request, 'soc/list_sp.html', context)

#docs about the quert set to order the cmt    
#https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by

def detail_sp(request,slug):
	context = {}

	service_provider   = get_object_or_404(Service_Provider, slug=slug)
	#this was something i want to remember about
	reviews             = Review.objects.filter(service_provider__slug=slug)
	# reviews             = Review.objects.filter(service_provider__slug=slug.order_by("-comment"))
	#we can now order it by using timestamp as the review model was updated.
	average             = reviews.aggregate(Avg("rating"))["rating__avg"]
	
	context = {
		"sp"        : service_provider,
		"reviews"   : reviews,
	}

	return render(request, 'soc/details.html', context)

# http://www.jeffreyteruel.com/article/3

def add_review(request, slug):
	
	# if request.user.is_authenticated:
		service_provider = Service_Provider.objects.get(slug=slug)
		if request.method == "POST":
			form = ReviewForm(request.POST or None)
			
			if form.is_valid():
				data                    = form.save(commit=False)
				data.comment            = request.POST["comment"]
				data.rating             = request.POST["rating"]
				data.user               = request.user
				data.service_provider   = service_provider
				data.save()
				return redirect("soc:details", slug)
			else:
				form = ReviewForm()
			return render(request, 'soc/details.html', {"form": form})
		else:
			return redirect('soc:home')    
 
#https://www.youtube.com/watch?v=lSX8nzu9ozg&list=PLeyK9Dw9ShReHUdt5Nh2qlgF6keN6DI7z&index=32

def edit_review(request, slug, review_id):
	if request.user.is_authenticated:
		service_provider    = Service_Provider.objects.get(slug=slug)
		
		review              = Review.objects.get(service_provider=service_provider, id = review_id)
		
		if request.user == review.user:
			#grant_permission
				form        = ReviewForm(request.POST, instance=review)
				if form.is_valid():
					data = form.save(commit=False)
					if(data.rating > 10) or (data.rating < 0):
						error = "out of range"
						return render(request, "soc/editreview.html", {"error":error, "form":form})
					else:
						data.save()
						return redirect("soc:details", slug)
				else:
					form = ReviewForm(instance=review)
				return render(request, "soc/editreview.html", {"form":form})
		else:
			return redirect("soc:home")

def delete_review(request, slug, review_id):
	if request.user.is_authenticated:
		service_provider    = Service_Provider.objects.get(slug=slug)
		review              = Review.objects.get(service_provider__slug=slug, id = review_id)
		if request.user == review.user:
			#grantpermision
			review.delete()
		return redirect("soc:details", slug)
	else:
		return redirect("soc:home")



def add_sp(request):
	context = {}
	print(request.POST)
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')
	if request.method == 'POST':
		form = SPForm(request.POST or None, request.FILES)
		if form.is_valid():
			data = form.save(commit=False)
			data.Posted_by = request.user
			data.save()
			return redirect("soc:home")
		else:
			form = SPForm()
			return redirect('soc:add_sp')
		context['form'] = form
	return render(request, "soc/add_sp.html", context)

