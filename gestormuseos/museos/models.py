from django.db import models

# Create your models here.

class Usuario(models.Model):
	nombre = models.CharField(max_length=128)
	color = models.CharField(max_length=128)
	fuente = models.IntegerField()
	titulo = models.CharField(max_length=128)
	def __str__(self):
			return self.nombre

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
	fecha = models.DateTimeField()
	def __str__(self):
		return self.usuario.nombre + ", " + self.museo.nombre + ", " + str(self.fecha)

class Comentario(models.Model):
	usuario = models.ForeignKey(Usuario)
	museo = models.ForeignKey(Museo)
	fecha = models.DateTimeField()
	comentario = models.TextField()
	def __str__(self):
		return self.usuario.nombre + ", " + self.museo.nombre + ", " + self.comentario