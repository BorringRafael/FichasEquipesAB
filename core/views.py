from django.shortcuts import render
from .models import Equipe, Profissional


def equipe(request):
    equipe_list = Equipe.objects.all()
    return render(request, 'core/equipe.html', {
                'equipe_list': equipe_list,
                })


def profissional(request, v1):
    if Profissional.objects.filter(equipe__ine=v1).exists():
        profissional_list = Profissional.objects.filter(equipe__ine=v1)
    else:
        profissional_list = Profissional.objects.filter(equipe__nome=v1)
    return render(request, 'core/profissional.html', {
                'profissional_list': profissional_list,
                })


def protocolo(request, v1, v2):
    profissional_filter = Profissional.objects.get(cns=v2)
    return render(request, 'core/ficha_protocolo.html', {
                'profissional_filter': profissional_filter,
                'linha': range(0, 56)
                })
