"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import *


urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='core/index.html'),
        name='core.index',
        ),
    url(
        r'^(?P<v1>\w+)/equipe/$',
        equipe,
        name='core.equipe',
        ),
    url(
        r'^(?P<v1>\w+)/profissional/(?P<v2>\w+)/$',
        profissional,
        name='core.profissional'
        ),
    url(
        r'^protocolo/capa/(?P<v2>\w+)/$',
        capa_protocolo,
        {"v1": "protocolo"},
        name='core.capa_protocolo',
        ),
    url(
        r'^protocolo/profissional/(?P<v2>\w+)/(?P<v3>\d{15})/$',
        ficha_protocolo,
        {"v1": "protocolo"},
        name='core.ficha_protocolo',
        ),
    url(
        r'^esus/atividade/(?P<v2>\w+)/$',
        ficha_atividade,
        {"v1": "protocolo"},
        name='core.ficha_atividade',
        ),
    url(
        r'^esus/profissional/(?P<v2>\w+)/(?P<v3>\d{15})/$',
        lista_ficha_esus,
        {"v1": "esus"},
        name='core.lista_ficha_esus',
        ),
    url(
        r'^esus/profissional/(?P<v2>\w+)/(?P<v3>\d{15})/(?P<v4>\w+)/$',
        ficha_esus,
        {"v1": "esus"},
        name='core.ficha_esus',
        ),
]
