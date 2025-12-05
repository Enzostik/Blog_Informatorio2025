"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'noticias'

urlpatterns = [
    path('', views.noticias, name='buscador'),
    path('<int:post_id>', views.ver_noticia, name='ver_noticia'),
    path('comments/<int:post_id>', views.comment_post, name='comentarios'),
    path('comments/edit', views.comment_edit, name='editar_comentario')
]