from tastypie.resources import ModelResource
from tastypie import fields
from listas.models import *



class UsuarioResource(ModelResource):
    class Meta:
        queryset = Usuario.objects.all()
        allowed_methods = ['get','put']

class SitioResource(ModelResource):
    class Meta:
        queryset = Sitio.objects.all()
        allowed_methods = ['get','put']

class ListaResource(ModelResource):
    sitio = fields.ToOneField(SitioResource, attribute='sitio', related_name='sitio')
    usuarios = fields.ToOneField(UsuarioResource, attribute='usuarios', related_name='usuarios')
    class Meta:
        queryset = Lista.objects.all()
        allowed_methods = ['get','put']
