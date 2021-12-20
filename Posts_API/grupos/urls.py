from django.urls import path

from .views import GrupoCreateAPIView, GrupoDeleteAPIView, GrupoDetailAPIView, GrupoListAPIView, GrupoUpdateAPIView


app_name = 'grupos-api'

urlpatterns = [

    path(r'list/', GrupoListAPIView.as_view(), name='grupo_list'),
    path(r'create/', GrupoCreateAPIView.as_view(), name='grupo_create'),
    path(r'<slug:slug>/', GrupoDetailAPIView.as_view(), name='grupo_detail'),
    path(r'<slug:slug>/update/', GrupoUpdateAPIView.as_view(), name='grupo_update'),
    path(r'<slug:slug>/delete/', GrupoDeleteAPIView.as_view(), name='grupo_delete'),
]

