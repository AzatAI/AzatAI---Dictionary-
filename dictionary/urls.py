from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", Main.as_view(), name="dict_main_url"),
    path("detail/<str:id>/<str:lang>", WordDetail.as_view(), name="word_detail_url"),
    path("notfound", NotFound.as_view(), name="not_found_url"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)