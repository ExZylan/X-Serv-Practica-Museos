from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.

class Usuario(models.Model):
	nombre = models.OneToOneField(User, related_name="usuario")
	color = models.CharField(max_length=128)
	tamano = models.IntegerField()
	titulo = models.CharField(max_length=128)
	fondo = models.CharField(max_length=128)
	def __str__(self):
			return self.nombre.username

class Museo(models.Model):
	nombre = models.CharField(max_length=128)
	enlace = models.CharField(max_length=128)
	direccion = models.CharField(max_length=5000)
	descripcion = models.TextField()
	accesible = models.IntegerField()
	barrio = models.CharField(max_length=128)
	distrito = models.CharField(max_length=128)
	telefono = models.CharField(max_length=128)
	fax = models.CharField(max_length=128)
	email = models.CharField(max_length=128)
	def __str__(self):
			return self.nombre

class Favorito(models.Model):
	usuario = models.ForeignKey(Usuario)
	museo = models.ForeignKey(Museo)
	fecha = models.DateTimeField(default = timezone.now())
	def __str__(self):
		return self.usuario.nombre.username + ", " + self.museo.nombre + ", " + str(self.fecha)

class Comentario(models.Model):
	usuario = models.ForeignKey(Usuario)
	museo = models.ForeignKey(Museo)
	fecha = models.DateTimeField(default = timezone.now())
	comentario = models.TextField()
	def __str__(self):
		return self.usuario.nombre.username + ", " + self.museo.nombre + ", " + self.comentario