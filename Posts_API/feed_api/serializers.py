
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ImageField
from rest_framework.relations import HyperlinkedRelatedField, StringRelatedField
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from comments.serializers import CommentSerializer

from .models import Likes, Postagem, UserImage 
from comments.models import Comment 


 #===========================================================================================================================================#
 # urls para linkar endpoints 

post_detail_url = HyperlinkedIdentityField( # link para detail url, podem ser usados em outros serializers apenas referenciando
        view_name='posts-api:detail',
        lookup_field='slug'
    )

categoria_detail_url = HyperlinkedRelatedField( # link para categoria
    read_only = True,
    view_name = 'grupos-api:grupo_detail',
    lookup_field = 'slug',
    source = 'categoria'
)

post_delete_url = HyperlinkedIdentityField( # link para deletar o post, apenas autor ou admin podem deletar
        view_name='posts-api:delete',
        lookup_field='slug'
    )
post_edit_url = HyperlinkedIdentityField( # link para editar o post, apenas autor ou admin podem deletar
        view_name='posts-api:update',
        lookup_field='slug'
    )

user_url  = HyperlinkedRelatedField(
        read_only=True,
        lookup_field = 'pk', 
        view_name='posts-api:user_detail',
        source = 'author'
    )

#===========================================================================================================================================#

class PostCreateUpdateSerializer(ModelSerializer):
    
    class Meta:
        model = Postagem 
        fields=[
            'title',
            'image',
            'conteudo',
            'categoria'
        ]

class PostListSerializer(ModelSerializer): #todo add comments counts and like eventually

    detail_url = post_detail_url
    author = SerializerMethodField()
    categoria = SerializerMethodField()
    categoria_url = categoria_detail_url
    image = SerializerMethodField()
    author_url = user_url
    comentarios = SerializerMethodField()
    image_perfil = ImageField(source='author.user_image_id.imagem_perfil')
    likes_count = SerializerMethodField()

    class Meta:
        model = Postagem 
        fields=[
            'detail_url', 
            'title',
            'image',
            'conteudo',
            'author',
            'author_url',
            'image_perfil',
            'timestamp',
            'categoria',
            'categoria_url',
            'comentarios',
            'likes_count'
        ]
    def get_author(self, obj):
        return str(obj.author.username)
    def get_categoria(self, obj):
        return(str(obj.categoria.group_name))
    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image
    def get_comentarios(self, obj):   #  contador de postagens e usuários por grupos. abrir detalhes para visualizar  
        count =  Comment.objects.filter(object_id = obj.id).count()
        return count
    def get_likes_count(self, obj):   #  contador de postagens e usuários por grupos. abrir detalhes para visualizar  
        count =  Likes.objects.filter(postagem = obj.id).count()
        return count
 


class PostDetailSerializer(ModelSerializer): # todo: add url to comments.. 

    delete_url = post_delete_url
    edit_url = post_edit_url 
    image = SerializerMethodField()
    author = SerializerMethodField()
    categoria_url = categoria_detail_url
    author_url = user_url
    comments = SerializerMethodField()
    image_perfil = ImageField(source='author.user_image_id.imagem_perfil')
    likes_count = SerializerMethodField()

    class Meta:
        model = Postagem 
        fields=[
            'id',
            'title',
            'image',
            'conteudo',
            'author',
            'author_url',
            'image_perfil',
            'timestamp',
            'categoria_url',
            'delete_url',
            'edit_url',
            'comments',
            'likes_count'
        ]
    def get_image(self, obj):
        try:
            image = obj.image.url 
        except:
            image = None
        return image
    def get_author(self, obj):
        return str(obj.author.username)
        
    def get_comments(self, obj):
        comments_qs = Comment.objects.filter(object_id = obj.id )
        comments = CommentSerializer(comments_qs, many=True).data
        return comments
    def get_likes_count(self, obj):   #  contador de postagens e usuários por grupos. abrir detalhes para visualizar  
        count =  Likes.objects.filter(postagem = obj.id).count()
        return count
 

user_detail_url = HyperlinkedIdentityField(
    view_name = 'posts-api:user_detail',
    lookup_field = 'pk'
)

#===========================================================================================================================================#

class UserSerializer(ModelSerializer):
    user_groups = StringRelatedField(many=True, read_only = True) #todo trocar por url para grupo (maybe )
    posts_count = SerializerMethodField()
    detail_url  = user_detail_url
    image_perfil = ImageField(source='user_image_id.imagem_perfil')
    
    class Meta:
        model = User
        fields = [
            'detail_url',
            'id',
            'username',
            'user_groups',
            'posts_count',
            'image_perfil',
            # comments_count
        ]



    def get_posts_count(self, obj):  
        count =  Postagem.objects.filter(author = obj).count()
        return count
# todo comments  

class UserDetailSerializer(ModelSerializer):
    user_groups = StringRelatedField(many=True, read_only = True)
    posts = HyperlinkedRelatedField(
        many=True,
        read_only=True,
        lookup_field = 'slug', 
        view_name='posts-api:detail',
        source = 'user_posts'
    )
    image_perfil = ImageField(source='user_image_id.imagem_perfil')
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'user_groups',
            'posts',
            'image_perfil',
  #          'comments'
        ]

class UserImageSerializer(ModelSerializer):
    class Meta:
        model = UserImage
        fields = [
            'imagem_perfil',
        ]

class LikeButtonSerializer(ModelSerializer):
    class Meta:
        model = Likes
        fields= '__all__'
    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['user'] in Likes.objects.all():
            raise ValidationError("finish must occur after start")
        return data