#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.sax import SAXParseException
import sys
import urllib.request
from museos.models import Museo


def normalize_whitespace(text):
    return string.join(string.split(text), ' ')


class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inContent = False
        self.theContent = ""
        self.attribute = ""
        self.first_museo = True
        #campos de un museo:
        self.nombre = ""
        self.enlace = ""
        self.direccion = ""
        self.descripcion = ""
        self.accesible = ""
        self.barrio = ""
        self.distrito = ""
        self.telefono = ""
        self.fax = ""
        self.email = ""

    def startElement (self, name, attrs):
        if name == 'contenido' and not self.first_museo: #guarda el museo anterior
            museo = Museo(nombre = self.nombre, descripcion = self.descripcion, accesible = self.accesible, enlace = self.enlace, direccion = self.direccion, barrio = self.barrio, distrito = self.distrito, telefono = self.telefono, fax = self.fax, email = self.email).save()

        if name == 'atributo':
            self.attribute = attrs.get("nombre")
        if self.attribute in ["NOMBRE", "DESCRIPCION", "ACCESIBILIDAD", "CONTENT-URL", "CLASE-VIAL", "BARRIO", "DISTRITO", "TELEFONO", "EMAIL", "FAX", "NOMBRE-VIA","NUM"]:
            self.inContent = True


    def endElement (self, name):

        if self.attribute == "NOMBRE":
            if self.first_museo:
                self.first_museo = False
            self.nombre = self.theContent
        elif self.attribute == "DESCRIPCION":
            self.descripcion = self.theContent
        elif self.attribute == "ACCESIBILIDAD":
            self.accesible = int(self.theContent)
        elif self.attribute == "CONTENT-URL":
            self.enlace = self.theContent

        # direccion
        elif self.attribute == "CLASE-VIAL":
            self.direccion = self.theContent + " " + self.direccion
        elif self.attribute == "NOMBRE-VIA":
            self.direccion += self.theContent + ", " + "NUM: "
        elif self.attribute == "NUM":
            self.direccion += self.theContent
        # fin direccion

        elif self.attribute == "BARRIO":
            self.barrio = self.theContent
        elif self.attribute == "DISTRITO":
            self.distrito = self.theContent

        # contacto
        elif self.attribute == "TELEFONO":
            if self.theContent != "":
                self.telefono = self.theContent
        elif self.attribute == "EMAIL":
            if self.theContent != "":
                self.email = self.theContent
        elif self.attribute == "FAX":
            if self.theContent != "":
                self.fax = self.theContent
        # fin contacto

        self.inContent = False
        self.theContent = ""


    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
