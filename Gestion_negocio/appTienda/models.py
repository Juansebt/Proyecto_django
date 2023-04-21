from django.db import models

# Create your models here.

class Categoria(models.Model):
    catNombre = models.CharField(max_length=50, unique=True)
    
class Producto(models.Model):
    proCodigo = models.IntegerField(unique=True)
    proNombre = models.CharField(max_length=50)
    proPrecio = models.IntegerField()
    proCategoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    proFoto = models.FileField(upload_to=f"images/", null=True, blank=True)