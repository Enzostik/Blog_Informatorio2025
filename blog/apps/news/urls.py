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
    # URLs para noticias
    path('buscar/', views.search_results, name='search_results'),
    path('<int:post_id>', views.ver_noticia, name='ver_noticia'),
    path('comentarios/<int:post_id>', views.comment_post, name='comentarios'),
    path('comentarios/editar/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('comentarios/eliminar/<int:comment_id>', views.delete_comment, name='delete_comment'),

    # URLs para categorías (para ser incluidas bajo el namespace 'categorias')
    path('lista/', views.category_list, name='category_list'),
    path('categoria/<int:category_id>/', views.news_by_category, name='news_by_category'),
]