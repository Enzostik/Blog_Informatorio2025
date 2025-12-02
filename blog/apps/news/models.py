from django.db import models
from apps.authuser.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class MainImage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, primary_key=True)
    image = models.ImageField(upload_to='images/')
    epigraph = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.title}({self.author}) el {self.creation_date}'

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"

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

    def __str__(self):
        return f"{self.title}({self.author})"

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"

class Comment(UserPost):
    post = models.ForeignKey(Publication, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)

    def __str__(self):
        return f'En {self.post} por {self.author} a las {self.last_update}'

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(UserPost)

    def __str__(self):
        return f'En {self.posts} por {self.user}'

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
