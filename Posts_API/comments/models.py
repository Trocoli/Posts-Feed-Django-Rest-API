from django.db import models


from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id= obj_id).filter(parent=None)
        return qs


class Comment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default=1, related_name='user')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent      = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)

    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


    def __unicode__(self):  
        return str(self.content)

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse("comments-api:thread", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("comments-api:delete", kwargs={"id": self.id})
        
    def children(self): #replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True