from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

PROVINCIAS=(('Buenos Aires','Buenos Aires'),
            ('Capital Federal','Capital Federal'),
            ('Catamarca','Catamarca'),
            ('Chaco','Chaco'),
            ('Chubut','Chubut'),
            ('Córdoba','Córdoba'),
            ('Corrientes','Corrientes'),
            ('Entre Ríos','Entre Ríos'),
            ('Formosa','Formosa'),
            ('Jujuy','Jujuy'),
            ('La Pampa','La Pampa'),
            ('La Rioja','La Rioja'),
            ('Mendoza','Mendoza'),
            ('Misiones','Misiones'),
            ('Neuquén','Neuquén'),
            ('Río Negro','Río Negro'),
            ('Salta','Salta'),
            ('San Juan','San Juan'),
            ('San Luis','San Luis'),
            ('Santa Cruz','Santa Cruz'),
            ('Santa Fe','Santa Fe'),
            ('Santiago del Estero','Santiago del Estero'),
            ('Tierra del Fuego','Tierra del Fuego'),
            ('Tucumán','Tucumán'),)

class User(AbstractUser):
    provincia = models.CharField(choices=PROVINCIAS, null=True, blank=True)