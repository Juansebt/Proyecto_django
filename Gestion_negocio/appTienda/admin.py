from django.contrib import admin
from appTienda.models import Producto, Categoria

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Producto)