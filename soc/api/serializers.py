from rest_framework import serializers
from soc.models import Service_Provider

class Service_PSerializer(serializers.ModelSerializer):

	class Meta:
		model = Service_Provider
		fields = ['name', 'panno', 'about', 'location', 'contactno', 'averageRating', 'image']
