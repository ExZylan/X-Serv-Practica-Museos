from django.shortcuts import render, redirect
from django.http import HttpResponse
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from museos.xml_parser import myContentHandler
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
import urllib.request
from django.template.loader import get_template
from django.template import Context

from django.contrib.auth import authenticate, login

from .models import Usuario, Museo, Favorito, Comentario

# Create your views here.

FILTROACCESIBLE = '''
            <form action="" Method="POST">
            <input type="submit" value="Accesibles">
</form>
'''

FILTROTODOS = '''
            <form action="" Method="GET">
            <input type="submit" value="Todos">
</form>
'''

FORMULARIO_COMENTARIOS = """
<form action= "" method="POST">
    Comentario: <input type="text" name="comentario">
    <input type= 'hidden' name='opcion' value='1'>
    <input type="submit" value="Enviar">
</form>
"""

@csrf_exempt
def Login_info(request):
    if request.user.is_authenticated():
        log = "<p>Logged in as " + request.user.username
        log += "<a href='/logout'> Logout </a></p>"
    else:
        log = "<form action='/login' method='post'>"
        log += "Usuario: <input type= 'text' name='user'><br>"
        log += "Contraseña: <input type= 'password' name='password'><br>"
        log += "<input type= 'submit' value='enviar'>"
        log += "</form>"
    return log

def seleccionafavorito(usuario, museo):
    favoritos = Favorito.objects.all()
    existe = False

    for favorit in favoritos:
        if str(favorit.museo.nombre) == str(museo):
            existe = True
            favorito =""
    if not existe:
        favorito = "<form action='/museos/" + str(museo.id) + "' Method='POST'><input type='submit' value='Like'><input type= 'hidden' name='usuarioo' value= " + usuario + "><input type= 'hidden' name='opcion' value='2'></form>"

    return favorito

@csrf_exempt
def Login(request):
    user = request.POST['user']
    password = request.POST['password']
    user = authenticate(username=user, password=password)
    if user is not None:
        login(request, user)
    return redirect("/")

def formfuente(usuario): 
    formulariofuente = """<form method='POST'>
                <b>Tamaño letra:</b>
                <select name='Letra'>
                    <option value='10'>10</option>
                    <option value='16'>16</option>
                    <option value='19'>19</option>
                    <option value='22'>22</option>
                    <option value='13'>Default(13)</option>
                </select>
                <input type= 'hidden' name='opcion' value='1'>
                <input type='submit' value='Enviar'>
            </form>
            <form method='POST'>
                <b>Color de fondo:</b>
                <select name='Color'>
                    <option value='blue'>Azul</option>
                    <option value='red'>Rojo</option>
                    <option value='white'>Blanco</option>
                    <option value='pink'>Rosa</option>
                    <option value='orange'>Naranja</option>
                    <option value='#1E1F21'>Default</option>
                </select>
                <input type= 'hidden' name='opcion' value='2'>
                <input type='submit' value='Enviar'>
            </form>"""

    return formulariofuente

def formtitulo(usuario):
    formulariotitulo = """<form method = 'POST'>
                <b><br>Titulo de la página:
                </b><br>
                <input type='text' name='Title'><br>
                <input type= 'hidden' name='opcion' value='3'>
                <input type='submit' value='Enviar'>
            </form>"""

    return formulariotitulo

def enlacespaginas(number, query, favoritos, cinco):
    respuesta = ""
    if cinco:
        respuesta = '<a href="' + str(number) + "?pag=" + str((int(query) + 1)) + '">' + "Página siguiente" + '</a>'
    if int(query) > 0: 
        respuesta += '<br><a href="' + str(number) + "?pag=" + str((int(query) + -1)) + '">' + "Página anterior" + '</a>'
    respuesta += '<br><a href="' + str(number) + "/XML" + '">' + "Mostrar xml" + '</a>'

    return respuesta

def listavoritos(favoritos, query, number, cinco):
    i=0
    museoinicio = int(query) * 5
    museofinal = (int(query) + 1) * 5 -1

    respuesta = "<ul>"
    for favorito in favoritos:
        if str(number) == str(favorito.usuario.id):
            if i >= museoinicio and i <= museofinal:
                respuesta += '<hr><a href="' + str(favorito.museo.enlace) + '">' + favorito.museo.nombre + "<br>" + '</a>' + favorito.museo.direccion + "<br>" + str(favorito.fecha) + "<br>" + '<a href="/museos/' + str(favorito.museo.id) + '">' + "Mas Información" + '</a>'
                respuesta += "</ul><ul>"
            if i == museofinal:
                cinco = True
            i = i+1

    return respuesta, cinco

def listarusuarios(usuarios):
    respuesta = "<h2>Lista de usuarios</h2>"
    for usuario in usuarios:
        respuesta += "<br><hr>" + str(usuario.nombre) + ": " + '<a href="usuario/' + str(usuario.id) + '?pag=0">' + usuario.titulo + '</a></hr>'

    return respuesta

def muestrainfo(museo, museos):
    comentarios = Comentario.objects.all()
    for nombre in museos:
        if museo in museos:
            if museo.accesible:
                accesible = "Si"
            else:
                accesible = "No"
            respuesta = "<ul><p>" + "Nombre: " + museo.nombre + "<br>Dirección: " + museo.direccion +  "<br>Barrio: " + museo.barrio + "<br>Distrito: " + museo.distrito + "<br>Accesibilidad: " + accesible + "<br>Contacto:<br>Teléfono: " + museo.telefono + "<br>Fax: " + museo.fax + "<br>Email: " + museo.email + "<br>Descripción: " + museo.descripcion + "<br>" + '<a href="' + str(museo.enlace) + '">' + "Enlace página web" + "<br>" + '</a></p>'
        respuesta += "<br> Comentarios: "
    for comentario in comentarios:
        if str(museo) == str(comentario.museo.nombre):
            respuesta += """<br><img src="/static/images/li.gif" alt="" />""" + comentario.comentario
    return respuesta

def filtraaccesibles(listaaccesibles, repeticiones):
    for repeticion in repeticiones:
        if repeticion[0] not in listaaccesibles:
            repeticiones.remove(repeticion)
    return repeticiones

def buscaaccesibles(comentarios):
    listaaccesibles = []
    for accesible in comentarios:
        if accesible.museo.accesible == 1:
            listaaccesibles.append(accesible.museo.nombre)
    return listaaccesibles

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
    repeticiones = {}
    for comentario in comentarios:
        if comentario.museo.nombre in repeticiones:
            repeticiones[comentario.museo.nombre] = repeticiones[comentario.museo.nombre] + 1
        else:
            repeticiones[comentario.museo.nombre] = 1
    repeticiones = [(k, repeticiones[k]) for k in sorted(repeticiones, key=repeticiones.get, reverse=True)]
    return repeticiones

def mascomentados(repeticiones):
    repe = 1
    museos = Museo.objects.all()
    respuesta = "<h2>¡Lista de museos más comentados!</h2><ul>"
    for repeticion in repeticiones:
        for museo in museos:
            if repeticion[0] == museo.nombre and repe <= 5:
                respuesta += '<hr><h1 class="Titulos"><a href="' + str(museo.enlace) + '">' + museo.nombre + "<br>" + '</a></h1>' + museo.direccion + "<br>" + '<a href="museos/' + str(museo.id) + '">' + "Mas Información" + '</a></hr>'
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
    usuarios = Usuario.objects.all()

    repeticiones = contador(comentarios)
    respuesta = mascomentados(repeticiones)
    listausuarios = listarusuarios(usuarios)
    boton = FILTROACCESIBLE
    
    if request.method == "POST":
        listaaccesibles = buscaaccesibles(comentarios)
        repeticiones = filtraaccesibles(listaaccesibles, repeticiones)
        respuesta = mascomentados(repeticiones)
        boton = FILTROTODOS

    #logueo = Login_info(request)

    template = get_template('redbridge/index.html');
    c = Context({'contenido': respuesta, 'login': Login_info(request), 'usuarios': listausuarios, 'accesibles': boton})
    return HttpResponse (template.render(c))


    #return HttpResponse(logueo + "<br>" + respuesta + "<br>" + listausuarios + "<br>" + boton)

@csrf_exempt
def museoslist(request):
    #logueo = Login_info(request)

    museos = Museo.objects.all()
    if request.method == "POST":
        museos = Museo.objects.filter(distrito=request.POST['distrito'])
    listadistritos = creadistritos(museos)
    respuesta = formulariodistritos(listadistritos)
    for museo in museos:
        respuesta += '<hr>'+ museo.nombre + '<a href="/museos/' + str(museo.id) + '">' + " Enlace a página" + '</a>'
    respuesta += "</ul><ul>" 

    template = get_template('redbridge/index.html');
    c = Context({'contenido': respuesta, 'login': Login_info(request)})
    return HttpResponse (template.render(c))
    
    #return HttpResponse(logueo + "<br>" + respuesta)
    

@csrf_exempt
def museo(request, number):
    if request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            comentario = Comentario(comentario = request.POST['comentario'], usuario = Usuario.objects.get(nombre = request.user), museo = Museo.objects.get(id=int(number)))
            comentario.save()
        elif opcion == "2":
            favorito = Favorito(museo = Museo.objects.get(id=int(number)), usuario = Usuario.objects.get(nombre = request.user))
            favorito.save()

    usuario = request.user.username

    logueo = Login_info(request)

    try:
        museos = Museo.objects.all()
        museo = Museo.objects.get(id=int(number))
        respuesta = muestrainfo(museo, museos)
        if request.user.is_authenticated():
            formulario = FORMULARIO_COMENTARIOS
            favorito = seleccionafavorito(usuario, museo)
        else:
            formulario = ""
            favorito = ""
    except Museo.DoesNotExist:
        return HttpResponse("no existe")

    template = get_template('redbridge/index.html');
    c = Context({'contenido': respuesta, 'login': Login_info(request), 'formulario': formulario, 'favorito': favorito})
    return HttpResponse (template.render(c))

    #return HttpResponse(logueo + "<br>" + respuesta + "<br>" + formulario + "<br>" + favorito)

@csrf_exempt
def usuario(request, number):
    usuario = Usuario.objects.get(id = number)
    if request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            usuario.tamano = request.POST['Letra']
        elif opcion == "2":
            usuario.color = request.POST['Color']
        elif opcion == "3":
            usuario.titulo = request.POST['Title']
        usuario.save()

    if usuario.nombre.username == request.user.username:
        formulariotitulo = formtitulo(usuario)
        formulariofuente = formfuente(usuario)

    else:
        formulariotitulo = "No eres propietario de la pagina"
        formulariofuente = ""

    query = request.GET.get('pag')
    cinco = False

    logueo = Login_info(request)

    favoritos = Favorito.objects.all()
    respuesta, cinco = listavoritos(favoritos, query, number, cinco)
    saltodepagina = enlacespaginas(number, query, favoritos, cinco)

    print(request.user.is_authenticated())
    print(request.user)

    #css = get_template('redbridge/images/style.css')
    template = get_template('redbridge/index.html');
    c = Context({'contenido': respuesta, 'login': Login_info(request), 'saltodepagina': saltodepagina, 'formulariotitulo': formulariotitulo, 'formulariofuente': formulariofuente})
    return HttpResponse (template.render(c))

    #return HttpResponse(logueo + "<br>" + respuesta + "<br>" + saltodepagina + "<br>" + formulariotitulo + "<br>" + formulariofuente)

def xml(request, number):
    favoritos = Favorito.objects.all()
    usuario = Usuario.objects.get(id = number)
    print(usuario)
    xml = """<?xml version="1.0" encoding="UTF-8" ?>\n\n\n"""
    xml += "\n<Contenidos>\n"
    for favorito in favoritos:
        if usuario.nombre.username == favorito.usuario.nombre.username:
            xml += "\t<contenido>\n"
            xml += """\t\t<atributo nombre = "NOMBRE">""" + favorito.museo.nombre + """</atributo>\n"""
            xml += """\t\t<atributo nombre = "DESCRIPCION-ENTIDAD">""" + favorito.museo.descripcion + """</atributo>\n"""
            xml += """\t\t<atributo nombre = "ACCESIBILIDAD">""" + str(favorito.museo.accesible) + """</atributo>\n"""
            print(favorito.museo.enlace)
            xml += """\t\t<atributo nombre = "CONTENT-URL">""" + "<![CDATA[" + favorito.museo.enlace + "]]>" + """</atributo>\n"""
            xml += """\t\t<atributo nombre = "LOCALIZACION">\n"""
            xml += """\t\t\t<atributo nombre = "DIRECCION">""" + favorito.museo.direccion + """</atributo>\n"""
            xml += """\t\t\t<atributo nombre = "BARRIO">""" + favorito.museo.barrio + """</atributo>\n"""
            xml += """\t\t\t<atributo nombre = "DISTRITO">""" + favorito.museo.distrito + """</atributo>\n"""
            xml += """\t\t</atributo>\n"""
            xml += """\t\t<atributo nombre = "DATOS-CONTACTOS">\n"""
            xml += """\t\t\t<atributo nombre = "TELEFONO">""" + favorito.museo.telefono + """</atributo>\n"""
            xml += """\t\t\t<atributo nombre = "FAX">""" + favorito.museo.fax + """</atributo>\n"""
            xml += """\t\t\t<atributo nombre = "EMAIL">""" + favorito.museo.email + """</atributo>\n"""
            xml += """\t\t</atributo>\n"""
            xml += "\t</contenido>\n"
    xml += "</Contenidos>"
    return HttpResponse(xml, content_type="text/xml")

@csrf_exempt
def about(request):
    respuesta = "<h2>Práctica final Mis museos</h2><br><hr>Esta pagina ha sido realizada con el fin de la entrega de la práctica final mis museos por el alumno Jesús Miguel del Álamo Albiol<br>Esta aplicacion contiene una base de datos de museos obtenida por la Comunidad de Madrid donde podrás buscar, valorar y guardar museos"

    template = get_template('redbridge/index.html');
    c = Context({'contenido': respuesta, 'login': Login_info(request)})
    return HttpResponse (template.render(c))

def css(request):
    #print(request.user)
    template = get_template('redbridge/images/style.css')
    color_user = "#1E1F21"
    letra_user = "12px"
    #print(request.user.id)
    #if request.user.is_authenticated():
    #    print("XXX")
        #usuario = User.objects.get(username=request.user)
        #color_user = Configuracion.objects.get(usuario=usuario).fondo
        #letra_user = str(Configuracion.objects.get(usuario=usuario).tamano)+'px'
    #print(color_user)
    c = Context({'Color': color_user, 'Letra': letra_user})

    return HttpResponse (template.render(c),content_type="text/css")