from tastypie.resources import ModelResource, Resource
from tastypie import fields
from tastypie.authorization import DjangoAuthorization, Authorization
import json

from listas.models import *

class UsuarioResource(ModelResource):
    class Meta:
        queryset = Usuario.objects.all()
        allowed_methods = ['get','put','post']

class SitioResource(ModelResource):
    class Meta:
        queryset = Sitio.objects.all()
        allowed_methods = ['get','put','post']
        authorization = Authorization()

class ListaResource(ModelResource):
    #sitio = fields.ToOneField(SitioResource, attribute='sitio', related_name='sitio')
    sitio = fields.CharField()
    usuarios = fields.CharField()
    #usuarios = fields.DictField()
    class Meta:
        queryset = Lista.objects.all()
        allowed_methods = ['get','put','post']
        authorization = Authorization()
    def dehydrate_sitio(self,bundle):
        print bundle.obj.sitio.nombre
        return str(bundle.obj.sitio.nombre)
    def dehydrate_usuarios(self,bundle):
        ret = {}
        for usuario in bundle.obj.usuarios.all():
            ret[usuario.nombre]=usuario.email
        #print ret
        return ret
    def hydrate(self, bundle):
        print "Establecemos el sitio"
        bundle.obj.sitio = Sitio.objects.get(nombre=bundle.data['sitio'])
        print "Vamos con los usuarios"
        usuarios = bundle.data['usuarios']
        bundle.obj.save()
        for nombre in usuarios:
            email = usuarios[nombre]
            print nombre,email
            u = Usuario(nombre=nombre,email=email)
            u.save()
            bundle.obj.usuarios.add(u)
        return bundle
        
