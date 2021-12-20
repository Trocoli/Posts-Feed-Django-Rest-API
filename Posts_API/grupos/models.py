from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import CharField
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Grupo(models.Model): # grupos, niveis diferentes de permissões 
    group_name = CharField(max_length=11)
    users = models.ManyToManyField(User, related_name='user_groups')
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.group_name
    class Meta:
        ordering = ["-id"]
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.group_name)
    if new_slug is not None:
        slug = new_slug
    qs = Grupo.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Grupo )
