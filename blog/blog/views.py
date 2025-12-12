from django.http.request import HttpRequest
from django.shortcuts import render

# Modelos de las publicaciones
from apps.news.models import Publication

#Error pages
def error_page(title:str, header:str, content:str, status:int):
    '''
    Decorator to render the HTML content of every error page.\n
    Only use with the functions:
        `page_not_found`,
        `bad_request`,
        `server_error`,
        `access_denied`
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            #Page content
            context = {
                'title_page' : title,
                'header_page' : header,
                'message' : content
            }
            #Get the request and exception of the main function
            request, exception = func(*args, **kwargs)
            #Render HTML with the custom content and status code
            return render(request, 'error_page.html', context, status=status)
        return wrapper
    return decorator

# Create your views here.
def index(request:HttpRequest):
    # Obtener las últimas 3 noticias para mostrar en la página principal
    publications = Publication.objects.order_by('-creation_date')[:3]
    # Lista de numeros para utilizar de referencia
    numbers = list(range(2, len(publications)+2))
    return render(request, 'index.html', context={ 'publications' : publications, 'numbers': numbers })

@error_page(
        'Página no encontrada',
        'ERROR 404 - Página no encontrada',
        'La página que ha intentado ingresar no existe o no puede accederse por el momento.',
        404
)
def page_not_found(request:HttpRequest, exception):
    return request, exception

@error_page(
        'Solicitud incorrecta',
        'ERROR 400 - Solicitud incorrecta',
        'Su solicitud es incorrecta o no permitida y no ha podido ser completada.',
        400
)
def bad_request(request:HttpRequest, exception):
    return request, exception

@error_page(
        'Error interno del servidor',
        'ERROR 500 - Error interno del servidor',
        'El servidor ha encontrado un problema para completar su solicitud.',
        500
)
def server_error(request:HttpRequest, exception=None):
    return request, exception

@error_page(
         'Acceso denegado',
         'ERROR 403 - Acceso denegado',
         'No posee los permisos para acceder a esta página.',
         403
)
def access_denied(request:HttpRequest, exception):
    return request, exception
