from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import Service_PSerializer
from soc.models import Service_Provider

#https://medium.com/@syarif.secondchance/vs-code-python-unresolved-import-warning-ea9bba3fa9af

@api_view(['GET', ])
def api_view_sp(request, slug):
    try:
        service_provider = Service_Provider.objects.get(slug=slug)
    except Service_Provider.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = Service_PSerializer(service_provider)
    return Response(serializer.data)

@api_view(['PUT', ])
def api_update_sp(request, slug):
    try:
        service_provider = Service_Provider.objects.get(slug=slug)
    except Service_Provider.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method== "PUT":
        serializer = Service_PSerializer(service_provider)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["sucess"] = "updated"
            return Response(data=data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
