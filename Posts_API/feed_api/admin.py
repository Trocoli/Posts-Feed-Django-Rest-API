from django.contrib import admin

# Register your models here.
from .models import Likes, Postagem, UserImage

class PostLikeAdmin(admin.TabularInline): # mostrar curtidas dentro da detail de postagens no admin
	model = Likes

class PostModelAdmin(admin.ModelAdmin):
	inlines = [PostLikeAdmin]
	list_display = ["title", "updated", "timestamp"]
	list_display_links = ["updated"]
	list_editable = ["title"]
	list_filter = ["updated", "timestamp"]

	search_fields = ["title", "conteudo"]
	class Meta:
		model = Postagem
		


admin.site.register(Postagem, PostModelAdmin)
admin.site.register(UserImage)