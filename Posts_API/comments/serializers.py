from rest_framework.fields import ImageField
from comments.models import Comment 
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'object_id',
            'content_type',
            'parent',
            'content',
        ]


class CommentSerializer(ModelSerializer):
    replies_count = SerializerMethodField()
    user = StringRelatedField(read_only = True)

    image_perfil = ImageField(source='user.user_image_id.imagem_perfil')
    class Meta:
        model = Comment 
        fields = [
            'id',
            'user',
            'image_perfil',
            'content_type',
            'object_id',
            'parent',
            'content',
            'replies_count',
            'timestamp',
        ]
    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):
    user = StringRelatedField(read_only = True)
    image_perfil = ImageField(source='user.user_image_id.imagem_perfil')
    class Meta:
        model = Comment 
        fields = [
            'id',
            'user',
            'content',
            'timestamp', 
            'image_perfil',
        ]

 

class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    replies_count = SerializerMethodField()
    image_perfil = ImageField(source='user.user_image_id.imagem_perfil')
    class Meta:
        model = Comment 
        fields = [
            'id',
            'content_type',
            'object_id',
            'content',
            'replies_count',
            'replies',
            'image_perfil',
        ]
    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None
    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
 

