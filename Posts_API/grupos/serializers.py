from django.contrib.auth.models import User
from feed_api.models import Postagem 
from rest_framework.relations import HyperlinkedRelatedField, StringRelatedField
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from .models import Grupo 


class GrupoCreateUpdateSerializer(ModelSerializer): # para o usuário ver postagens no field é preciso atribuir grupos a esse usuário
    class Meta:
        model = Grupo
        fields = [
            'group_name',
            'users'
        ]

#===========================================================================================================================================#

class GrupoListSerializer(ModelSerializer): 
    detail_url = HyperlinkedIdentityField( # pega a url para detail view
        read_only=True,
        view_name='grupos-api:grupo_detail',
        lookup_field='slug',
    )
    postagens = SerializerMethodField()
    users = SerializerMethodField()
    class Meta:
        model = Grupo
        fields =[
            'detail_url',
            'group_name',
            'users',
            'postagens'
            ]
 
    def get_postagens(self, obj):   #  contador de postagens e usuários por grupos. abrir detalhes para visualizar  
        count =  Postagem.objects.filter(categoria = obj).count()
        return count

    def get_users(self, obj): # contador de usuários. detalhes na detail acessada através de 'groups/slug'
        count =  User.objects.filter(user_groups  = obj).count()
        return count

#===========================================================================================================================================#

class GrupoDetailSerializer(ModelSerializer): #visão mais detalhada de usuarios e postagens 

    users = StringRelatedField(many=True)
    posts_grupos = HyperlinkedRelatedField( # detail viewl mostra urls para a detail view das postagens feitas nesse grupo
        many=True,
        read_only=True,
        lookup_field = 'slug', 
        view_name='posts-api:detail',
    )

    class Meta:
        model = Grupo
        fields = [
            'group_name',
            'users',
            'posts_grupos'
        ]
