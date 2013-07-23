# -*- coding: utf-8 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

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
        nombre_sitio=bundle.data['sitio']
        #print "Establecemos el sitio con el nombre %s"%nombre_sitio
        bundle.obj.sitio = Sitio.objects.get(nombre=nombre_sitio)
        #print "Vamos a procesar los usuarios"
        usuarios = bundle.data['usuarios']
        #primero hacemos un save porque sino no nos deja hacer el usuarios.add
        bundle.obj.save()
        for nombre in usuarios:
            email = usuarios[nombre]
            usuario,created = Usuario.objects.get_or_create(nombre=nombre,email=email)
            #if created:
            #    print "Creando el usuario %d %s-%s"%(usuario.id,usuario.nombre,usuario.email)
            #else:
            #    print "Ya existia el user %d %s-%s"%(usuario.id,usuario.nombre,usuario.email)
            #print "Añadimos el user"
            bundle.obj.usuarios.add(usuario)
        return bundle
        
