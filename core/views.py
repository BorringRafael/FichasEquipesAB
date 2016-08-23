from django.shortcuts import render
from .models import Equipe, Profissional


def equipe(request, v1):
    equipe_list = Equipe.objects.all()
    return render(request, 'core/equipe.html', {
                'equipe_list': equipe_list,
                'v1': v1,
                })


def profissional(request, v1, v2):
    if Profissional.objects.filter(equipe__ine=v2).exists():
        profissional_list = Profissional.objects.filter(equipe__ine=v2)
    else:
        profissional_list = Profissional.objects.filter(equipe__nome=v2)
    return render(request, 'core/profissional.html', {
                'profissional_list': profissional_list,
                'v1': v1,
                'v2': v2,
                })


def capa_protocolo(request, v1, v2):
    if Equipe.objects.filter(ine=v2).exists():
        equipe = Equipe.objects.filter(ine=v2)
    else:
        equipe = Equipe.objects.filter(nome=v2)
    return render(request, 'core/capa_protocolo.html', {
                'equipe': equipe,
                })


def ficha_protocolo(request, v1, v2, v3):
    profissional_filter = Profissional.objects.get(cns=v3)
    return render(request, 'core/ficha_protocolo.html', {
                'profissional_filter': profissional_filter,
                'v1': v1,
                'linha': range(0, 56)
                })
