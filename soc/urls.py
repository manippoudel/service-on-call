from django.urls import path
from rest_framework.urls import app_name

from . import views
from .views import (add_review, delete_review, detail_sp, edit_review,
                    home_view, list_sp)

app_name = 'soc'

urlpatterns = [
    path('', home_view.as_view(), name='home'),
    path('serviceproviders/', views.list_sp, name='list'),
    path('serviceproviders/details/<slug>/', views.detail_sp, name='details'),
    path('serviceproviders/addreview/<slug>/', views.add_review, name='add_review'),
    path('serviceproviders/editreview/<slug>/<int:review_id>', views.edit_review, name='edit_review'),
    path('serviceproviders/deletereview/<slug>/<int:review_id>', views.delete_review, name='delete_review'),
    

]

