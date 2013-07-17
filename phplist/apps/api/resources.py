from tastypie.resources import ModelResource, Resource
from tastypie import fields

import json

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
    #sitio = fields.ToOneField(SitioResource, attribute='sitio', related_name='sitio')
    sitio = fields.CharField()
    usuarios = fields.DictField()
    class Meta:
        queryset = Lista.objects.all()
        allowed_methods = ['get','put']
    def dehydrate_sitio(self,bundle):
        print bundle.obj.sitio.nombre
        return str(bundle.obj.sitio.nombre)
    def dehydrate_usuarios(self,bundle):
        ret = {}
        for usuario in bundle.obj.usuarios.all():
            ret[usuario.nombre]=usuario.email
        print ret
        return ret
