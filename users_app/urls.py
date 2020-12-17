from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from dictionary.views import WordView

urlpatterns = [
    path("", Main.as_view(), name="main_url"),
    path("main/", include('dictionary.urls')),
    path("registration/", Registration.as_view(), name="registration_user_url"),
    path("login/", Login.as_view(), name="log_user_url"),
    path("logout/", Logout.as_view(), name="logout_url"),
    path("api/words/", WordView.as_view(), name="word_view_url"),
    path("api/device/", DeviceView.as_view(), name="device-view-url"),
    path("api/users/<str:ver>/", UsersView.as_view(), name="user_view_url"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)