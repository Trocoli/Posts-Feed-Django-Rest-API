#ex2021_2_MicrosFEED_Douglas URL Configuration

from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('feed_api.urls', namespace='posts-api' )),
    path('groups/' , include('grupos.urls', namespace='grupos-api' )),
    path('comments/' , include('comments.urls', namespace='comments-api' ))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)