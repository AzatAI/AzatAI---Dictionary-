from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", Main.as_view(), name="main_url"),
    path("registration/", Registration.as_view(), name="registration_user_url"),
    path("login/", Login.as_view(), name="log_user_url"),
    path("logout/", Logout.as_view(), name="logout_url"),
    path("my-account/", MyAccount.as_view(), name="my_account_url"),
    path("api/users/<str:ver>/", UsersView.as_view(), name="user_view_url"),
    path("api/device/", DeviceView.as_view(), name="device-view-url"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)