from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.deletion import PROTECT
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from comments.models import Comment
from grupos.models import Grupo 

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name = 'user_like')
    postagem = models.ForeignKey("Postagem", on_delete=models.CASCADE, related_name='post_liked', default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"

class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_image_id')
    imagem_perfil = models.ImageField(upload_to="images_perfil/%Y/%m/%d/", null=True, blank=True)

    class Meta:
        verbose_name = "User Image"
        verbose_name_plural = "User Images"
    
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" %(new_id, filename)


class Postagem(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='publicado')

    options = (
        ('rascunho','Rascunho'), ('publicado','Publicado')
    )

    title = models.CharField(max_length=200, blank=False, null = False)
    image = models.ImageField(upload_to="images_posts/%Y/%m/%d/", null=True, blank=True)#, height_field='50', width_field='100') TAVA DANDO ERRO
    conteudo = models.TextField(blank=False,null=False)
    categoria = models.ForeignKey(Grupo,on_delete=PROTECT, default=1, related_name='posts_grupos')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    slug = models.SlugField(unique=True) #url identificador para usar no lugar do ID qnd for usar chave estrangeira
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_posts'
    )
    likes = models.ManyToManyField(User, blank=True,  related_name='post_likes', through=Likes)

    #image_perfil = models.ForeignKey(UserImage, related_name='image_perfil')
    #UserImage.objects.get_or_create(user=author.primary_key))

    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    objects = PostManager() # default manager
    postobjects = PostObjects() # custom manager 
    class Meta:
        ordering = ('-timestamp', '-updated')
        verbose_name = "Postagem"
        verbose_name_plural = "Postagens"
        
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]


@property
def comments(self):
    instance = self
    qs = Comment.objects.filter_by_instance(instance)
    return qs

@property
def get_content_type(self):
    instance = self
    content_type = ContentType.objects.get_for_model(instance.__class__)
    return content_type

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Postagem.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Postagem )





