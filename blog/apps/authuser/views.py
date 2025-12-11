from django.http.request import HttpRequest

# Para manejar urls
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse

# Mostrar mensajes
from django.contrib import messages

# Para manejar permisos
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import User
from django.contrib.auth.models import Permission

# Cargar formularios
from .forms import RegisterForm, LoginForm

# Modelo de publicaciones
from apps.news.models import Publication

def check_redirect(request:HttpRequest, next:str = None)->HttpResponseRedirect :
    '''
    Funcion para verificar si la redirección es segura y dentro del dominio de la app.\n
    
    Args
    ----
    request : HttpRequest
        Pedido HTML del cliente.
    next : str
        URL a redirigir. Si no se carga un valor intentará obtenerla del parámetro `?next=` de la URL.

    Returns
    -------
        HttpResponseRedirect : 
        A la página `next` si está cargada y es segura, o a `home` de lo contrario
    '''
    # Páginas que requieran iniciar sesión llamarán la funcion login_page()
    # y esta funcion redireccionará a la página original.
    if not next:
        next = request.GET.get('next')
    if next and url_has_allowed_host_and_scheme(url=next,
                                                allowed_hosts=request.get_host(),
                                                require_https=request.is_secure()):
        return redirect(next)
    # Si no hay variable o no es una redirección segura volver a página de inicio
    return redirect('home')

# Create your views here.
def register_user(request:HttpRequest):
    '''
    Pagina para registrar usuario.\n
    Carga `register.html`\n
    Si se completo el formulario de inicio de sesión llama `check_redirect` a la página principal o a la página cargada en la variable `next`
    '''
    #Si el usuario ya tiene una sesión iniciada redirigir a la página principal
    if request.user.is_authenticated:
        return redirect('home')

    #Si el cliente ha enviado el formulario de registro
    if request.method == 'POST':
        #Obtener el formulario del cliente
        form = RegisterForm(request.POST)
        #Si los datos son válidos, al correr clean() del formulario RegisterForm
        if form.is_valid():
            #Obtener los datos para crear el usuario
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')

            #Crear objeto user
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name)
            #Escribir un mensaje para indicar al usuario que su cuenta fue creada exitosamente y ahora debe iniciar sesión
            #Dicho mensaje se cargará en la variable 'messages' del request
            messages.add_message(request, messages.SUCCESS,
                                 "Cuenta creada exitosamente. Ingrese su usuario y contraseña para iniciar sesión.",
                                 'success')

            # Si hay variable next en la url pasarla al login
            return redirect('usuario:login' if not request.GET.get('next') else 
                            reverse('usuario:login')+f"?next={request.GET.get('next')}")
        else:
            #TODO: Agregar los mensajes de campos no válidos del formuario
            for item in form.errors.as_data().values():
                messages.add_message(request, messages.ERROR, item[0].message, 'danger')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form' : form})

def login_user(request:HttpRequest):
    '''
    Página para inicio de sesión\n
    Carga `login.html`\n
    Si se completo el formulario de inicio de sesión llama `check_redirect` a la página principal o a la página cargada en la variable `next`
    '''
    #Si el usuario ya tiene una sesión iniciada redirigir a la página principal
    if request.user.is_authenticated:
        return redirect('home')
    
    #Si el usuario envió el formulario de inicio de sesión proceder a obtener los datos
    if request.method=='POST':
        #Cargar el formulario
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            #Verificar que el usuario y contraseña exista en la base de datos
            user = authenticate(username=username, password=password)
            if user is not None:
                #Si el usuario existe iniciar sesión
                login(request, user)
                #Si no se ha marcado la opción para recordar la sesión, la misma terminará al cerrar el navegador
                if not remember_me:
                    request.session.set_expiry(0)
                #Regresar un redirect a la página principal o a next_page si es segura
                return check_redirect(request)
            #Si no se ha logrado obtener el usuario, agregar un mensaje de error y renderizar la página con dicho mensaje
            messages.add_message(request, messages.ERROR, 'Usuario o contraseña incorrecto.', 'danger')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form' : form})

def logount_user(request:HttpRequest):
    '''
    Verifica si el usuario tiene una sesión iniciada y la termina.\n
    Regresa a la `página principal`
    '''
    #Si el usuario tiene una sesión iniciada terminarla
    if request.user.is_authenticated:
        logout(request)
    #Regresar a la página principal
    return redirect('home')

@login_required
def profile(request:HttpRequest):
    '''
    Página del perfil del usuario.\n
    Carga `profile.html`
    '''
    #Uso del decorador login_required que verifica si el usuario está autenticado
    # Publicaciones del usuario
    publications = Publication.objects.filter(author=request.user)
    #Redirige a settings.LOGIN_URL con el parámetro 'next' en caso contrario
    return render(request, 'user/profile.html', context={ 'publications': publications })

def view_user(request:HttpRequest, id_value:int):
    try:
        user_obj = User.objects.get(pk=id_value)
    except:
        raise Http404
    # Publicaciones del usuario
    publications = Publication.objects.filter(author=user_obj)
    # Revisar si el usuario es él mismo o es staff
    context = {'user_obj': user_obj, 'publications': publications }
    return render(request, 'user/user.html', context)
