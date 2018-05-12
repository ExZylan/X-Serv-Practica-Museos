from django.shortcuts import render
from django.http import HttpResponse
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from museos.xml_parser import myContentHandler
from django.views.decorators.csrf import csrf_exempt
import urllib.request

from .models import Usuario, Museo, Favorito, Comentario

# Create your views here.

formulario ="""
<form action= "" method="POST">
    Destino: <input type="text" name="desti">
    Locomocion: <input type="text" name="loco" value ="Avion">
    Alojamiento: <input type="text" name="aloj">
    Precio: <input type="text" name="pre">
    <input type="submit" value="Enviar">
</form>
"""

@csrf_exempt
def cargar_museos(request):
    museos = Museo.objects.all()
    for museo in museos:
        museos.delete()

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    xmlFile = urllib.request.urlopen("https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full")
    theParser.parse(xmlFile)

    return HttpResponse("Cargado")

@csrf_exempt
def barra(request):
    museos = Museo.objects.all()

    respuesta = "<ul>"
    for museo in museos:
        respuesta += '<li><a href="' + str(museo.enlace) + '">' + museo.nombre + "<br>" + '</a>' + museo.direccion + "<br>" + '<a href="museos/' + str(museo.id) + '">' + "Mas Información" + '</a>'
    respuesta += "</ul>"

    return HttpResponse(respuesta)