from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from django.utils.text import slugify
from django.template.defaultfilters import slugify
import base64






# def upload_location(instance, filename):
#i can make it more usable by allowing user to upload multiple photos, contact no,

class Service_Provider(models.Model):
	name            =  models.CharField(max_length=100)
	panno           =  models.CharField(max_length=30, unique=True,blank=True, null=False)
	about           =  models.TextField(max_length=50)
	location        =  models.CharField(max_length=100)
	contactno       =  models.CharField(max_length=10,unique=True)
	averageRating   =  models.FloatField(default=0)#need to remove
	image           =  models.ImageField(upload_to='sp_pics')
	is_approved		=  models.BooleanField(default=False)
	date_joined		= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	date_updated 	= models.DateTimeField(auto_now=True, verbose_name="date updated")
	Posted_by		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)		
	slug			= models.SlugField(unique=True, editable=False)


# fields = ('name', 'panno', 'location', 'about', 'image', 'contactno')

	#https://www.youtube.com/watch?v=lSX8nzu9ozg&list=PLeyK9Dw9ShReHUdt5Nh2qlgF6keN6DI7z&index=32
 
 #multiple photos
 #https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django

	def __str__(self):
		return self.name


	class Meta:
		verbose_name 		= 'Service Provider'
		verbose_name_plural = 'Service Provider'
	# def save(self,*args,**kwargs):
	# 	super(Service_Provider,self).save(*args,**kwargs)
	# 	if not self.slug:
	# 		self.slug = slugify(self.name+'-'+str(self.id))
	# 		super(Service_Provider,self).save(*args,**kwargs)
 #wecanencode the field
	def save(self,*args,**kwargs):
		if not self.slug:
			#this is used to check the ValueError
			# breakpoint()
			self.slug = slugify(self.name+'-'+self.panno)
		super(Service_Provider,self).save(*args,**kwargs)
 
	# @property
	# def review(self):
	# 	return self.review_set.all()

# #it helps to check the pre existing foelds or not
# def pre_save_sp(sender, instance, *args, **kwargs):
# 	if not instance.slug:
# 		instance.slug = slugify(instance.name + "-" +  str(instance.object.id))
  
# pre_save.connect(pre_save_sp, sender=Service_Provider)


class Review(models.Model):
	service_provider = models.ForeignKey(Service_Provider, on_delete=models.CASCADE)
	user 			 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
	comment  		 = models.TextField(max_length=800)
	rating 			 = models.FloatField(default=0)
	timestamp		 = models.DateTimeField(auto_now_add=True)
	#integer field can be consider for best use

	def __str__(self):
		return self.user.username

	def is_allowed(self, user):
		return self.user == user

	@property
	def user_name(self):
	 	return self.user.username
class about_member(models.Model):
	name		= models.CharField(max_length=30)
	expertise 	= models.TextField(max_length=15)
	fb_link 	= models.CharField(max_length=100)
	tw_link 	= models.CharField(max_length=100)
	lk_link 	= models.CharField(max_length=100)
	image 		= models.ImageField(upload_to='member_pics')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name 		= 'About Member'
		verbose_name_plural = 'About Member'

class home_page(models.Model):
	slider_image 	= models.ImageField(upload_to='slider_pics')
	sliding_text	= models.TextField(max_length=30)

	def __str__(self):
		return self.sliding_text

	class Meta:
		verbose_name 		= 'Home Page'
		verbose_name_plural = 'Home Page'
