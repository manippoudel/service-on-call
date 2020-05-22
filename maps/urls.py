from django.urls import path
from .views import maps
from . import views

urlpatterns = [
    path('maps/', views.maps, name='maps')
]
