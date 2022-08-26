from rest_framework import serializers
from soc.models import Service_Provider, Review

import cv2
import sys
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_PANNO_LENGTH = 50
MIN_CONTACT_NO_LENGTH = 10


class  Review_SPSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= Review
		fields	= ['id','service_provider', 'user', 'rating','comment', 'timestamp']
  
class ReviewSP_Detail(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField()
    
    class Meta():
        model = Review
        fields = ['id', 'service_provider', 'user_name', 'rating', 'comment', 'timestamp']

class Service_PSerializer(serializers.ModelSerializer):

	review = Review_SPSerializer(many=True)

	# image   = serializers.SerializerMethodField('get_username_from_Posted_by')
	class Meta:
			model = Service_Provider
			fields = ['pk', 'name', 'panno', 'slug', 'about', 'location', 'contactno', 'averageRating', 'image', 'review',]
	def validate_image_url(self, service_provider):
		image = service_provider.image
		new_url	= image.url
		if "?" in new_url:
			new_url = image.url[:image.url.rfing("?")]
		return new_url

class ServiceProviderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Provider
        fields = ['name', 'panno', 'slug', 'image', 'location', 'about', 'contactno']
  
class ServiceProviderUpdateSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Service_Provider
		fields = ['pk', 'name', 'panno', 'slug', 'about', 'location', 'contactno', 'averageRating', 'image',]

	def validate(self, service_provider):
		try:
			# panno = service_provider['title']
			# if len(title) < MIN_PANNO_LENGTH:
			# 	raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			# contact_no = service_provider['body']
			# if len(contact_no) < MIN_CONTACT_NO_LENGTH:
			# 	raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
			
			image = service_provider['image']
			url = os.path.join(settings.TEMP , str(image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()

			if sys.getsizeof(image.file) > IMAGE_SIZE_MAX_BYTES:
				os.remove(url)
				raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			img = cv2.imread(url)
			dimensions = img.shape # gives: (height, width, ?)
			
			aspect_ratio = dimensions[1] / dimensions[0] # divide w / h
			if aspect_ratio < 1:
				os.remove(url)
				raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
		except KeyError:
			pass
		return service_provider
  
class Service_ProviderCreateSerializer(serializers.ModelSerializer):
	

	class Meta:
		model = Service_Provider
		fields = [ 'name', 'panno',  'about', 'location', 'contactno', 'image','Posted_by']

		def save(self):
			try:
				image = self.validated_data['image']
				# panno = self.validated_data['panno']
				# if len(panno) < MIN_PANNO_LENGTH:
				# 	raise serializers.ValidationError({"response": "Enter a panno longer than " + str(MIN_PANNO_LENGTH) + " characters."})
				
				# contact_no = self.validated_data['contact_no']
				# if len(contact_no) < MIN_CONTACT_NO_LENGTH:
				# 	raise serializers.ValidationError({"response": "Enter a contact no longer than " + str(MIN_CONTACT_NO_LENGTH) + " characters."})
				
				service_provider = Service_Provider(
														Posted_by=self.validated_data['Posted_by'],
														name=name,
														panno=panno,
														contactno=contactno,
														image=image,
														about=about,
														location=location,
													)

				url = os.path.join(settings.TEMP , str(image))
				storage = FileSystemStorage(location=url)

				with storage.open('', 'wb+') as destination:
					for chunk in image.chunks():
						destination.write(chunk)
					destination.close()

				if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
					os.remove(url)
					raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
				if not is_image_aspect_ratio_valid(url):
					os.remove(url)
					raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

				os.remove(url)
				service_provider.save()
				return service_provider
			except KeyError:
				raise serializers.ValidationError({"response": "You must have primary"})
