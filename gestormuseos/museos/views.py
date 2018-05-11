from django.shortcuts import render
from django.http import HttpResponse
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from museos.xml_parser import myContentHandler
from django.views.decorators.csrf import csrf_exempt
import urllib.request

from .models import Usuario
from .models import Museo
from .models import Favorito
from .models import Comentario

# Create your views here.

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