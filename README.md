# Blog_Informatorio2025
Proyecto final del Grupo 1 de la Comisión 2 del Informatorio 2025

Página Web de tipo blog, para publicar noticias.

## Requerimientos
* **Python >= 3.10**
  * `pillow >= 12.0.0`
  * `asgiref >= 3.10.0`
  * `Django >= 5.2.8`
  * `pillow >= 12.0.0`
  * `sqlparse >= 0.5.3`
  * `tzdata >= 2025.2`

## Uso de producción
Si se empleará el proyecto empleando un servicio de alojamiento, cambiar en `blog\manage.py` la variable del entorno (línea 9) `blog.settings.local` a `blog.settings.production` y realizar las configuraciones que requiera el servicio de alojamiento para definir las páginas y recursos.

```python
# Cambiar de:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings.local')
# Al valor:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings.production')
```