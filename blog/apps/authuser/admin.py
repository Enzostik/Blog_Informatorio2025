from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

# Registrar el modelo del nuevo usuario
# admin.site.register(User)
@admin.register(User)
class NewUserAdmin(admin.ModelAdmin):
    pass
