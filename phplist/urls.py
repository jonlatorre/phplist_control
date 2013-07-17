from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

#La API
from api.resources import *
from tastypie.api import Api
v1_api = Api(api_name='v1')
v1_api.register(SitioResource())
v1_api.register(UsuarioResource())
v1_api.register(ListaResource())


handler500 = "pinax.views.server_error"

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^listas/', include('listas.urls')),
    url(r'^api/', include(v1_api.urls)),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
