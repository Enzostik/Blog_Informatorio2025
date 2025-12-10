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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # Importar TemplateView
from . import views
# Configurar página 'media' para imágenes subidas
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('acerca-de/', TemplateView.as_view(template_name='about.html'), name='about'), # Página Acerca de
    path('contacto/', TemplateView.as_view(template_name='contact.html'), name='contact'), # Página Contacto
    # Incluir las páginas definidas por las otras apps
    path('noticias/', include('apps.news.urls')),
    path('categorias/', include('apps.news.urls', namespace='categorias')), # URLs para categorías
    path('', include('apps.authuser.urls')),
    
]

# Agregar media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#Error pages
handler400 = views.bad_request
handler403 = views.access_denied
handler404 = views.page_not_found
handler500 = views.server_error
