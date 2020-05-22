from django.urls import path

from .views import api_view_sp

app_name = 'soc'

urlpatterns = [
    path('<slug>/',api_view_sp, name="detail"),
]
