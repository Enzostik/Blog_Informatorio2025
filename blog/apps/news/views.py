import json
from django.http.request import HttpRequest
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

# Modelos de las publicaciones
from .models import Publication, Comment

# Create your views here.
def noticias(request:HttpRequest):
    all_publications = Publication.objects.all().order_by('-creation_date')
    return render(request, 'noticias/noticias.html', context={'publicaciones': all_publications})

def ver_noticia(request:HttpRequest, post_id:int):
    publication = Publication.objects.get(pk=post_id)
    return render(request, 'noticias/ver_noticia.html', context={'publication': publication})

def commentar_post(request:HttpRequest, post_id:int):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            http_comments = HttpResponse()
            comments = Comment.objects.filter(post_id=post_id)
            if len(comments) > 0:
                for comment in comments:
                    http_comments.write(
                        f'\n<p>Por {comment.author} el {comment.creation_date}</p>'\
                        f'\n<p>{comment.content}</p>'\
                        f'\n<p>Ultima actualización el {comment.last_update}</p>'
                    )
            else:
                http_comments.write(
                    '<p>Esta publicación no tiene comentarios.</p>'
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