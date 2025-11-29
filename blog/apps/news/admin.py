from django.contrib import admin
from .models import Category, MainImage, Publication, Comment, LikePost

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(MainImage)
class MainImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'creation_date')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'creation_date', 'last_update')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'creation_date', 'last_update')

@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ['user']
