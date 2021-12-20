
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import render

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView
)

from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentCreateSerializer, CommentDetailSerializer, CommentChildSerializer, CommentSerializer
from .serializers import CommentCreateSerializer, CommentDetailSerializer, CommentSerializer
from .models import Comment 

#todo add comment delete 
#===========================================================================================================================================#
class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
#todo gotta get obj id from request and get content type auto 
#===========================================================================================================================================#

class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

#===========================================================================================================================================#

class CommentDetailView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAdminUser]

    ## todo add comment delete and permission classes. 



class CommentDeleteAPIView(DestroyAPIView): 
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdminUser]
    lookup_field = 'pk'