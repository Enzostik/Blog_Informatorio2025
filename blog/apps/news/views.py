import json
from django.utils import timezone
from django.http.request import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q # Importar Q para consultas OR
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied # Importar PermissionDenied
from django.urls import reverse # Importar reverse

from django.http import HttpResponse, JsonResponse

# Modelos de las publicaciones
from .models import Publication, Comment, Category # Importar el modelo Category para la gestión de categorías

# Create your views here.
def ver_noticia(request:HttpRequest, post_id:int):
    publication = Publication.objects.get(pk=post_id)
    return render(request, 'noticias/ver_noticia.html', context={'publication': publication})

def search_results(request:HttpRequest):
    query = request.GET.get('q')
    results = []
    if query:
        # Filtrar publicaciones por título, ignorando mayúsculas/minúsculas
        results = Publication.objects.filter(
            Q(title__icontains=query)
        ).order_by('-creation_date')
    else:
        query = 'todas las noticias.'
        results = Publication.objects.all().order_by('-creation_date')
    return render(request, 'noticias/search_results.html', {'query': query, 'results': results})

# Vista para listar todas las categorías disponibles
def category_list(request:HttpRequest):
    categories = Category.objects.all().order_by('name')
    return render(request, 'noticias/category_list.html', {'categories': categories})

# Vista para mostrar noticias filtradas por una categoría específica
def news_by_category(request:HttpRequest, category_id:int):
    # Obtener la categoría, o devolver un 404 si no existe
    category = get_object_or_404(Category, pk=category_id)
    # Filtrar publicaciones que pertenecen a la categoría, ordenadas por fecha de creación
    publications = Publication.objects.filter(category=category).order_by('-creation_date')
    return render(request, 'noticias/news_by_category.html', {'category': category, 'publications': publications})

def comment_post(request:HttpRequest, post_id:int):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            http_comments = HttpResponse()
            comments = Comment.objects.filter(post_id=post_id)
            if len(comments) > 0:
                for comment in comments:
                    http_comments.write(
                        '<div class="card mb-3">'
                        '<div class="card-body">'
                        f'<p class="card-text">Por <strong>{comment.author}</strong> el {comment.creation_date.strftime("%d %b, %Y a las %H:%M")}</p>'
                        f'<p class="card-text">{comment.content}</p>'
                        f'<p class="card-text"><small class="text-muted">Última actualización el {comment.last_update.strftime("%d %b, %Y a las %H:%M")}</small></p>'
                    )
                    # Agrerar botones editar/borrar si el usuario es autor o staff
                    if request.user.is_authenticated and (request.user == comment.author or request.user.is_staff):
                        http_comments.write(
                            '<div class="mt-2">'
                            f'<a href="{reverse("noticias:edit_comment", args=[comment.pk])}" class="btn btn-sm btn-outline-primary me-2"><i class="fa-solid fa-edit"></i> Editar</a>'
                            f'<a href="{reverse("noticias:delete_comment", args=[comment.pk])}" class="btn btn-sm btn-outline-danger"><i class="fa-solid fa-trash-alt"></i> Eliminar</a>'
                            '</div>'
                        )
                    http_comments.write('</div></div>') # Cerrar card body y card
            else:
                http_comments.write(
                    '<p class="text-muted">Esta publicación no tiene comentarios.</p>'
                )
            return http_comments
        #POST requiere header con 'X-CSRFToken' con el token actual
        elif request.method == 'POST' and request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                content = str(data['comment'])
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            if len(content.strip()) > 0:
                new_comment = Comment(author=request.user, post_id = post_id, content = content)
                new_comment.save()
                return JsonResponse({'success': True}, status=200)
    return HttpResponse('Invalid AJAX request.', status=400)

@login_required
def edit_comment(request:HttpRequest, comment_id:int):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Revisar permisos de edición: solo autor o staff
    if not (request.user == comment.author or request.user.is_staff):
        raise PermissionDenied("No tienes permiso para editar este comentario.")

    if request.method == 'POST':
        edited_content = request.POST.get('content', '').strip()
        if edited_content:
            comment.content = edited_content
            comment.last_update = timezone.now()
            comment.save()
            return redirect('noticias:ver_noticia', post_id=comment.post.pk) # Redirigir a la página de la publicación
        else:
            # Manejo de errores pero no implementado
            pass

    return render(request, 'noticias/edit_comment.html', {'comment': comment})

@login_required
def delete_comment(request:HttpRequest, comment_id:int):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Revisar permisos de eliminación: solo autor o staff
    if not (request.user == comment.author or request.user.is_staff):
        raise PermissionDenied("No tienes permiso para eliminar este comentario.")

    if request.method == 'POST':
        post_id = comment.post.pk # Obtener el ID de la publicación antes de eliminar el comentario
        comment.delete()
        return redirect('noticias:ver_noticia', post_id=post_id) # Redirigir a la página de la publicación

    return render(request, 'noticias/confirm_delete_comment.html', {'comment': comment}) # Confirmación
