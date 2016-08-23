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
from .views import equipe, profissional, ficha_protocolo, capa_protocolo


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
        r'^(?P<v1>\w+)/capa/(?P<v2>\w+)/$',
        capa_protocolo,
        name='core.capa_protocolo'
        ),
    url(
        r'^(?P<v1>\w+)/profissional/(?P<v2>\w+)/(?P<v3>\d{15})/$',
        ficha_protocolo,
        name='core.ficha_protocolo'
        ),
]
