from django.views.generic import TemplateView
from .models import (
    about_member,
    home_page,
    Service_Provider,
    Review,
)
from django.shortcuts import get_object_or_404, render,redirect
from .forms import *


#what if i make different views and pass it to snippets and call the snippets: remember to try it
#for example about us lai euta snippets banara euta view ma rakhera herne prayas garr
# def about_us(request):
#     context= {}
#     about = 
#.orderby('-')


#this part deals with the Service Provider and their views in website section.
class home_view(TemplateView):
    template_name = "soc/index.html"

    def get_context_data(self, **kwargs):
        context         = super(home_view, self).get_context_data(**kwargs)
        context['sps']   = Service_Provider.objects.filter(is_approved=True)
        context['hps']   = home_page.objects.all()
        context['ams']   = about_member.objects.all()
        return context

def list_sp(request):
    context = {}
    allsp = Service_Provider.objects.filter(is_approved=True)
    context = {
        "sp": allsp, 
    }
    return render(request, 'soc/list_sp.html', context)
    
def detail_sp(request,slug):
    context = {}

    service_provider   = get_object_or_404(Service_Provider, slug=slug)
    #this was something i want to remember about
    reviews            = Review.objects.filter(service_provider__slug=slug)
    
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
        service_provider = Service_Provider.objects.get(slug=slug)
        
        review       = Review.objects.get(service_provider=service_provider, id = review_id)
        
        if request.user == review.user:
            #grantpermision
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("soc:details", slug)
                else:
                    form = ReviewForm(instance=review_sp)
                return render(request, "soc/editreview.html", {"form":form})
            else:
                return redirect("details", slug)
        else:
            return redirect("home")

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



                
                
                
                

