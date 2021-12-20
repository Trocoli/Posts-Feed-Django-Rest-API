from django.contrib.auth.models import User
from functools import reduce
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404) 

from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.views import APIView
from feed_api.models import Postagem
from grupos.models import Grupo
from .serializers import LikeButtonSerializer, PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer, UserDetailSerializer, UserImageSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly
from .models import Likes, UserImage


class PostCreateAPIView(CreateAPIView):
    queryset = Postagem.objects.all()
    serializer_class = PostCreateUpdateSerializer 
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) # Associa automaticamente usuário logado como dono da postagem


class PostDetailAPIView(RetrieveAPIView): # post detail view, uses the slug instead of ID 
    queryset = Postagem.objects.all()
    serializer_class = PostDetailSerializer 
    lookup_field = 'slug' 


class PostUpdateAPIView(UpdateAPIView): #post update, uses slug, saves author automatically 
    queryset = Postagem.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdminUser] # IsAuthorOrReadOnly -> custom permission feito no arquivo permissions.py para permitir apenas o criador da postagem editá-la ou excluí-la

    lookup_field = 'slug'
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDeleteAPIView(DestroyAPIView): 
    queryset = Postagem.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [ IsAdminUser, IsAuthorOrReadOnly]
    lookup_field = 'slug' 


class PostListAPIView(ListAPIView):
    queryset = Postagem.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields = ['title' ,'conteudo' ,  'author__username', 'timestamp',]


    def get_queryset(self, *args, **kwargs):    # custom queryset para exibir no feed principal apenas postagens dos grupos no qual o user faz parte.
        user = self.request.user # pega a query do usuário logado
        grupos = Grupo.objects.filter(users=user) # checa os grupos a qual o usuário pertence
        query = Postagem.objects.filter(categoria__id__in=grupos) # checa se a categoria(nome do grupo no models de postagem) está presente no queryset dos grupos do usuário
        return query


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

class UserImageUpdateView(UpdateAPIView): # View para inserção ou update de imagem de perfil.
    queryset = UserImage.objects.all()
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk) 
        try:
            UserImage.objects.create(user=user)
        except:
            pass
            
        return super().update(request, *args, **kwargs)
        
    
class PostLikeAPIView(APIView): # funciona com um 'toggle', cada vez que um request for dado a opção de curtir adciona ou remove um like
    queryset = Likes.objects.all()
    serializer_class = LikeButtonSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Postagem, slug=slug) # pega a postagem pelo slug 
        user = self.request.user
        updated = False
        liked = False
        if user in obj.likes.all():
            liked = False
            obj.likes.remove(user)
        else:
            liked = True
            obj.likes.add(user)
        updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)