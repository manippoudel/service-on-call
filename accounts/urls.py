from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView
from django.urls import path

from .views import account_view, login_view, logout_view, registration_view, must_authenticate_view

urlpatterns = [
    path("register/",registration_view,name="register"),
    path("logout/",logout_view,name="logout"),
    path("login/",login_view,name="login"),
    path("update/",account_view,name="update"),
    path("must_authenticate/",must_authenticate_view,name="must_authenticate"),


    path("password-reset/",auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html')),
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),

]
