from django.conf.urls import include
from django.urls import path

from comments.views import CommentDeleteAPIView, CommentDetailView, CommentListAPIView, CommentCreateAPIView
app_name = 'comments-api'

urlpatterns = [
    path('list/', CommentListAPIView.as_view(), name ='list'),
    path('create/', CommentCreateAPIView.as_view(), name ='create'),
    path('<int:pk>/', CommentDetailView.as_view(), name ='thread'),
    path('<int:pk>/delete', CommentDeleteAPIView.as_view(), name ='delete')
]