from django.urls import path

from .views import  api_detail_view_sp, APISPListView, sp_registration_view, add_review_sp, edit_review_sp,sp_detail_api

app_name = 'soc'

urlpatterns = [
    path('listsp',APISPListView.as_view(), name="listsp"),
    path('detailsp/<slug>/',api_detail_view_sp, name="detail"),
    path('registersp',sp_registration_view, name="register"),
    #for review section
	path('addreview/<slug>/',add_review_sp,name="addreview"),
    path('editreview/<slug>/<int:review_id>',edit_review_sp,name="editreview"),
    path('spreview/<slug>',sp_detail_api,name="review")

    #user id and timestamp encode
]
