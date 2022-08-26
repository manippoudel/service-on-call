from django.urls  import  path
from accounts.api.views import (
    account_properties_view,
    account_update,
    ObtainAuthTokenView,
    registration_view,
    
    
)
app_name = "accounts"

urlpatterns = [
    path('register', registration_view, name="register"),
    path('properties', account_properties_view, name="properties"),
    path('properties/update', account_update, name="update"),
    path('login', ObtainAuthTokenView.as_view(), name="login"), # -> see accounts/api/views.py for response and url info
]
