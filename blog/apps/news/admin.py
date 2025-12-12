from django.contrib import admin
from .models import Category, MainImage, Publication, Comment, LikePost

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(MainImage)
class MainImageAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display = ('title', 'author', 'creation_date')

    def save_model(self, request, obj, form, change):
        # Si no es creación del objecto definir al usuario como el actual
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display = ('title', 'author', 'creation_date', 'last_update')

    def save_model(self, request, obj, form, change):
        # Si no es creación del objecto definir al usuario como el actual
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'creation_date', 'last_update')

@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ['user']
