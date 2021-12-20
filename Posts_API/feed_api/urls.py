from django.conf.urls import include
from django.urls import path

from feed_api.views import PostDetailAPIView, PostLikeAPIView, PostListAPIView, PostUpdateAPIView, PostDeleteAPIView, PostCreateAPIView, UserDetailAPIView, UserListAPIView, UserImageUpdateView

app_name = 'posts-api'

urlpatterns = [
    #endpoints de criação e listagem
    path(r'create/', PostCreateAPIView.as_view(), name='create'), #create post
    path(r'', PostListAPIView.as_view() , name='list'),
    # endpoints de usuário
    path(r'users/', UserListAPIView.as_view(), name='user_list'),
    path(r'users/<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path(r'users/<int:pk>/image_perfil/', UserImageUpdateView.as_view(), name='user_image'),
    # endpoint de like
    path(r'<slug:slug>/like/', PostLikeAPIView.as_view(), name='like'),
    #endpoint de detail view update ou destroy
    path(r'<slug:slug>/', PostDetailAPIView.as_view(), name='detail'),
    path(r'<slug:slug>/edit', PostUpdateAPIView.as_view(), name='update'),
    path(r'<slug:slug>/delete', PostDeleteAPIView.as_view(), name='delete'), 

]
