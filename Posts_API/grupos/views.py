from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView)

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import filters
from rest_framework.permissions import IsAdminUser
from grupos.serializers import  GrupoCreateUpdateSerializer, GrupoDetailSerializer, GrupoListSerializer
from .models import Grupo 

#===========================================================================================================================================#

class GrupoCreateAPIView(CreateAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoCreateUpdateSerializer
    permission_classes = [IsAdminUser]

#===========================================================================================================================================#

class GrupoUpdateAPIView(UpdateAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoCreateUpdateSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'

#===========================================================================================================================================#

class GrupoDeleteAPIView(DestroyAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoCreateUpdateSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'


#===========================================================================================================================================#

class GrupoListAPIView(ListAPIView):
    serializer_class = GrupoListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        queryset = Grupo.objects.filter(users=user)
        return queryset 
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['group_name', 'slug'] 

#===========================================================================================================================================#

class GrupoDetailAPIView(RetrieveAPIView):
    queryset = Grupo.objects.all() 
    serializer_class = GrupoDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
