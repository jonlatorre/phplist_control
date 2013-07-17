from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=25)
    email = models.EmailField()
    def __unicode__(self):
        return "%s"%self.nombre
    def get_absolute_url(self):
        return "/listas/usuarios/%d/"%self.id
    
class Sitio(models.Model):
    dominio = models.CharField(max_length=100)
    nombre = models.CharField(max_length=25)
    def __unicode__(self):
        return "%s"%self.nombre
    def get_absolute_url(self):
        return "/listas/sitios/%d/"%self.id


class Lista(models.Model):
    sitio = models.ForeignKey(Sitio)
    nombre = models.CharField(max_length=25)
    usuarios =  models.ManyToManyField(Usuario)
    def __unicode__(self):
        return "%s"%self.nombre
    def get_absolute_url(self):
        return "/listas/%d/"%self.id
