from django.shortcuts import render, redirect
from django.db import Error
from appTienda.models import Categoria
from appTienda.models import Producto
from django.conf import settings
import os

# Create your views here.

def inicio(request):
    return render(request, "inicio.html")

#---------------------------------------------------------------------------------------------------------------------------
#CATEGORIA
#---------------------------------------------------------------------------------------------------------------------------
def vistaCategoria(request):
    return render(request, "frmCategoria.html")

def agregarCategoria(request):
    nombre = request.POST["txtNombre"]
    estado = False
    
    try:
        categoria = Categoria(catNombre=nombre)
        categoria.save()
        mensaje = f"Categoria agregada correctamente"
        estado =  True
    except Error as error:
        mensaje = f"Problemas al agregar la categoría {error}"
    
    retorno = {"estado":estado,"mensaje":mensaje}
    
    return render(request, "frmCategoria.html", retorno)

#---------------------------------------------------------------------------------------------------------------------------
#PRODUCTO
#---------------------------------------------------------------------------------------------------------------------------
def listarProductos(request):
    mensaje = f""
    estado = False
    
    try:
        productos = Producto.objects.all()
        estado = True
        # print(productos)
    except Error as error:
        mensaje = f"Problemas al obtener los productos {error}"
        
    retorno = {"mensaje":mensaje,"estado":estado,"listaProductos":productos}
    
    return render(request,"listarProductos.html",retorno)

def vistaProducto(request):
    mensaje = ""
    estado = False
    
    try:
        categorias = Categoria.objects.all()
        estado = True
    except Error as error:
        mensaje = f"Problemas al obtener las categorias de los productos {error}"
        
    retorno = {"mensaje":mensaje,"estado":estado,"listaCategorias":categorias,"producto":None}
    
    return render(request,"frmProducto.html",retorno)

def agregarProducto(request):
    nombre = request.POST["txtNombreP"]
    codigo = int(request.POST["txtCodigo"])
    precio = int(request.POST["txtPrecio"])
    idCategoria = int(request.POST["cbCategoria"])
    # archivo = request.FILES["fileFoto"]
    archivo = request.FILES.get("fileFoto", False)
    mensaje = ""
    estado = False
    
    try:
        categoria = Categoria.objects.get(id=idCategoria) #Se obtienen las categorias
        producto = Producto(proNombre=nombre,proCodigo=codigo,
                            proPrecio=precio,proCategoria=categoria,
                            proFoto=archivo) #Se creael producto
        #Registro en la base de datos
        producto.save()
        mensaje = f"Producto agregado correctamente"
        estado = True
        return redirect("/listarProductos/")
    except Error as error:
        mensaje = f"Problemas al agregar un producto {error}"
        
    categorias = Categoria.objects.all()
    retorno = {"mensaje":mensaje,"estado":estado,"listarCategorias":categorias,"producto":producto}
    return render(request,"frmProducto.html",retorno)

def consultarProducto(request, id):
    # mensaje = ""
    # estado = False
    try:
        producto = Producto.objects.get(id=id)
        categorias = Categoria.objects.all()
        mensaje = ""
        # estado = True
    except Error as error:
        mensaje = f"Problemas al consultar {error}"
        
    retorno = {"mensaje":mensaje,"producto":producto,"listaCategorias":categorias}
    return render(request,"frmEditarProducto.html",retorno)

def actualizarProducto(request):
    idProducto = int(request.POST["idProducto"])
    nombre = request.POST["txtNombreP"]
    codigo = int(request.POST["txtCodigo"])
    precio = int(request.POST["txtPrecio"])
    idCategoria = int(request.POST["cbCategoria"])
    archivo = request.FILES.get("fileFoto", False)
    mensaje = ""
    estado = False
    try:
        categoria = Categoria.objects.get(id=idCategoria)
        
        producto = Producto.objects.get(id=idProducto)
        
        producto.proNombre = nombre
        producto.proPrecio = precio
        producto.proCategoria = categoria
        producto.proCodigo = codigo
        
        if(archivo):
            if (producto.proFoto):
                # rutaFile = producto.proFoto.path #Se recupera la ruta del archivo
                # os.remove(rutaFile)
                producto.proFoto.storage.delete(producto.proFoto.name)
            producto.proFoto = archivo
        else:
            producto.proFoto = producto.proFoto
        producto.save()
        mensaje = f"Producto actualizado correctamente"
        estado = True
        return redirect("/listarProductos/")
    except Error as error:
        mensaje = f"Problemas al actualizar el producto {error}"
    categorias = Categoria.objects.all()
    retorno = {"mensaje":mensaje,"estado":estado,"listaCategorias":categorias,"producto":producto}
    return render(request,"frmEditarProducto.html",retorno)

def eliminarProducto(request, id):
    mensaje = ""
    estado = False
    try:
        producto = Producto.objects.get(id=id)
        
        rutaFile = (producto.proFoto.url).split("/") #Recuperamos la URL de la foto y se divide
        ruta = "\\"+str(rutaFile[2])+"\\"+str(rutaFile[3]) #Se construye una ruta de archivo
        
        os.remove(os.path.join(settings.MEDIA_ROOT+ruta))
        #Módulo os para eliminar un archivo ubicado en la ruta especificada, que se construye uniendo la configuración MEDIA_ROOT del módulo settings de Django con la variable "ruta"
        
        # producto.proFoto.storage.delete(producto.proFoto.name)

        producto.delete()
        mensaje = f"Producto eliminado"
        estado = True
    except Error as error:
        mensaje = f"Problemas al eliminar el producto {error}"
        
    retorno = {"mensaje":mensaje,"estado":estado}
    return redirect("/listarProductos/",retorno)