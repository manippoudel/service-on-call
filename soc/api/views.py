from rest_framework import status
from rest_framework.decorators import api_view,permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import  ListAPIView
from .serializers import (
	Service_ProviderCreateSerializer,
	ServiceProviderListSerializer,
	Service_PSerializer,
	Review_SPSerializer,
 	ReviewSP_Detail,
	ServiceProviderUpdateSerializer,
)
from soc.models import Service_Provider, Review
from rest_framework.authentication import TokenAuthentication
from rest_framework import  serializers
from soc.models import Service_Provider
from rest_framework.filters import  SearchFilter, OrderingFilter

#https://medium.com/@syarif.secondchance/vs-code-python-unresolved-import-warning-ea9bba3fa9af

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def sp_registration_view(request):
	if request.method == 'POST':
		data = request.data
		data['Posted_by'] = request.user.pk
		serializer = Service_ProviderCreateSerializer(data=data)
		data = {}

		if serializer.is_valid():
			service_provider = serializer.save()
			data['response'] = "Successfully Registered"
			data['pk'] = service_provider.pk
			data['slug'] = service_provider.slug
			data['name'] = service_provider.name
			data['panno'] = service_provider.panno
			data['location'] = service_provider.location
			data['about'] = service_provider.about
			data['contactno'] = service_provider.contactno
			data['username'] = service_provider.Posted_by.username
			data['date_updated'] = service_provider.date_updated
			image_url = str(request.build_absolute_uri(service_provider.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			return Response(data=data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_view_sp(request, slug):
	try:
		service_provider = Service_Provider.objects.get(slug=slug)
	except Service_Provider.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		serializer = ServiceProviderListSerializer(service_provider)
		return Response(serializer.data)

@api_view(['PUT', ])
def api_update_sp(request, slug):
	try:
		service_provider = Service_Provider.objects.get(slug=slug)
	except Service_Provider.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	if request.method== "PUT":
		serializer = ServiceProviderUpdateSerializer(service_provider, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data["success"]  = "updated"            
			data["name"]    = service_provider.name
			data["panno"]    = service_provider.panno
			data["contact_no"]    = service_provider.contact_no
			data["date_updated"]    = service_provider.date_updated
			
			image_url = str(request.build_absolute_uri(service_provider.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
				return Response(data=data)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
def api_delete_sp(request, slug):
	try:
		service_provider = Service_Provider.objects.get(slug=slug)
	except Service_Provider.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	if request.method== "DELETE":
		serializer = Service_PSerializer(service_provider)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data["sucess"] = "updated"
			return Response(data=data)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class APISPListView(ListAPIView):
	queryset                = Service_Provider.objects.all()
	serializer_class        = ServiceProviderListSerializer
	authentication_classes  = (TokenAuthentication,)
	permission_classes      = (IsAuthenticated,)
	pagination_class        = PageNumberPagination
	
	filter_backends         = (SearchFilter,OrderingFilter)
	search_fields           = ('name', 'panno', 'location')
	
class APISP_DetailView():
	serializer_class = Service_PSerializer
	
	def get_queryset(self):
		queryset = Service_Provider.objects.all()
		return super().get_queryset()
	
	
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def add_review_sp(request, slug):
	# service_provider = Service_Provider(slug=slug)
	if request.method == "POST":
		data 				= request.data.copy()
		data['user'] 	= request.user.pk
		data["service_provider"] = Service_Provider.objects.get(slug=slug).pk
		print(request.data)
		print(data)
		serializer 			= Review_SPSerializer(data=data)
		data = {}
		if serializer.is_valid():
			review_sp 			= serializer.save()
			data['response']	= 'Review Added Successfully'
			data['pk']			= review_sp.pk
			data['comment']		= review_sp.comment
			data['rating']		= review_sp.rating
			data['timestamp']	= review_sp.timestamp
			return Response(data=data)
		return Response(serializer.errors, status=400)
#for this part in front end we have to check for request.user.pk vs review.user.pk
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def edit_review_sp(request, slug, review_id):
	if request.method == "POST":
		data = request.data.copy()
		data['user'] 	= request.user.pk
		data["service_provider"] = Service_Provider.objects.get(slug=slug).pk
		review = Review.objects.get(service_provider=data["service_provider"], id = review_id)
		# if request.user == review.user :
		if review.is_allowed(request.user):
			print(request.POST)
			print(data)
			serializer =  Review_SPSerializer(data=data)
			if serializer.is_valid():
				review_sp = serializer.save()
				data['response'] : 'Review Updated Successfully'
				data['pk'] : review_sp.pk
				data['comment'] : review_sp.comment
				data['rating']		= review_sp.rating
				data['timestamp']	= review_sp.timestamp
				return Response(data=data)
		return Response(data={'response':'Not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def sp_detail_api(request, slug):
	try:
		service_provider = Service_Provider.objects.get(slug=slug)
	except Service_Provider.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	reviews = Review.objects.filter(service_provider=service_provider)
	serializer = ReviewSP_Detail(reviews,many=True)
	return Response(serializer.data)
	























# class ReviewServiceProviderViewSet(viewsets.ModelViewSet):
#     serializer_class = Review_SPSerializer
	
#     def get_queryset(self):
#         return Review.objects.filter(
#             service_provider__slug=self.request.slug
#         )
		
#     def create(self, request, pk=None):
#             service_provider = Service_Provider.objects.get(id=service_provider_slug)
#             serializer = Review_SPSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(service_provider=service_provider)
#                 return Response(serializer.data)
#             else:
#                 return Response(serializer.errors,
#                                 status=status.HTTP_400_BAD_REQUEST)

#         def retrieve(self, request, pk=None):
#             service_provider = Service_Provider.objects.get(pk=pk)
#             serializer = PasswordSerializer(contact.contactphonenumber_set.all(), many=True)
#             return Response(serializer.data)
	# @action(methods=['post'], detail=False)
	# def add_review_to_sp(self, request, id=service_provider_id):
	#     service_provider    = Service_Provider.objects.get(id=service_provider_id)
	#     serializer          = Review_SPSerializer(data=request.data)
	#     if serializer.is_valid():
	#         serializer.save(service_provider=service_provider)
	#         return Response(serializer.data)
	#     else:
	#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
	# @action(methods=['get'], detail=False)
	




