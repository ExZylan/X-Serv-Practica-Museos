from django.shortcuts import render
from django.http import HttpResponse
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from museos.xml_parser import myContentHandler
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
import urllib.request

from .models import Usuario, Museo, Favorito, Comentario

# Create your views here.

def formulariodistritos(listadistritos):
    respuesta = "<ul>" + """<form action="" method="post">Distrito:<select name="distrito">"""
    for i in range(len(listadistritos)):
        respuesta += """<option value="""
        respuesta += listadistritos[i]
        respuesta += """>""" + listadistritos[i] + """</option>"""
    respuesta += """ </option></select><input type="submit" value="Enviar"><br></form>"""

    return respuesta

def creadistritos(museos):
    listadistritos = []
    for museo in museos:
        if museo.distrito not in listadistritos:
            listadistritos.append(museo.distrito)
    return listadistritos


def contador(comentarios):
    repeticiones ={}
    for comentario in comentarios:
        if comentario.museo.nombre in repeticiones:
            repeticiones[comentario.museo.nombre] = repeticiones[comentario.museo.nombre] + 1
        else:
            repeticiones[comentario.museo.nombre] = 1
    repeticiones = OrderedDict(sorted(repeticiones.items()))
    return repeticiones

def mascomentados(repeticiones):
    repe = 1
    museos = Museo.objects.all()
    respuesta = "<ul>"
    for repeticion in repeticiones.keys():
        for museo in museos:
#            print (repeticion)
            if repeticion == museo.nombre and repe <= 5:
                respuesta += '<li><a href="' + str(museo.enlace) + '">' + museo.nombre + "<br>" + '</a>' + museo.direccion + "<br>" + '<a href="museos/' + str(museo.id) + '">' + "Mas Información" + '</a>'
                repe = repe + 1
        respuesta += "</ul><ul>" 
    return respuesta

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
    comentarios = Comentario.objects.all()

    repeticiones = contador(comentarios)
    respuesta = mascomentados(repeticiones)

    return HttpResponse(respuesta)

@csrf_exempt
def museoslist(request):
    i=0
    museos = Museo.objects.all()
    if request.method == "POST":
        museos = Museo.objects.filter(distrito=request.POST['distrito'])
    listadistritos = creadistritos(museos)
    respuesta = formulariodistritos(listadistritos)
    for museo in museos:
        respuesta += '<li> '+ museo.nombre + '<a href="' + str(museo.enlace) + '">' + " Enlace a página" + '</a>'
    respuesta += "</ul><ul>" 
    
    return HttpResponse(respuesta)
    

@csrf_exempt
def museo(request, number):
    try:
        museo = Museo.objects.get(id=int(number))
    except Museo.DoesNotExist:
        return HttpResponse("no existe")
    return HttpResponse("no rula")