import json
from django.utils import timezone
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

def comment_post(request:HttpRequest, post_id:int):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'GET':
            http_comments = HttpResponse()
            comments = Comment.objects.filter(post_id=post_id)
            if len(comments) > 0:
                for comment in comments:
                    http_comments.write(
                        '<div>'\
                        f'\n<p>Por {comment.author} el {comment.creation_date}</p>'\
                        f'\n<p>{comment.content}</p>'\
                        f'\n<p>Ultima actualización el {comment.last_update}</p>'\
                        f"\n{f'<button comment={comment.pk}>Editar</button>' if comment.author == request.user else ''}"\
                        '</div>'
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

def comment_edit(request:HttpRequest):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST' and request.user.is_authenticated():
            try:
                data = json.loads(request.body)
                comment = Comment.objects.get(data['comment-id'])
                if not request.user.is_staff() or not (comment.author == request.user):
                    return HttpResponse('Invalid user permissions', status=401)
                if data['delete-comment']:
                    comment.delete()
                else:
                    comment.content = str(data['edited-comment'])
                    comment.last_update = timezone.now()
                    comment.save()
            except:
                return HttpResponse('An error has ocurred.', status=500)
    return HttpResponse('Invalid AJAX request.', status=400)