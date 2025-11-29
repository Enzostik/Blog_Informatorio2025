from django.db import models
from apps.authuser.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

class MainImage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, primary_key=True)
    image = models.ImageField(upload_to='images/')
    epigraph = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)

class UserPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_update = models.DateTimeField(auto_now=True)

class Publication(UserPost):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=250)
    body = models.TextField()
    image = models.OneToOneField(MainImage, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(UserPost):
    post = models.ForeignKey(Publication, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)

class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(UserPost)
