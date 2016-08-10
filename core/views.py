from django.shortcuts import render
from .models import Equipe, Profissional


def equipe(request):
    equipe_list = Equipe.objects.all()
    return render(request, 'core/equipe.html', {
                'equipe_list': equipe_list,
                })


def profissional(request, ine):
    profissional_list = Profissional.objects.filter(equipe__ine=ine)
    return render(request, 'core/profissional.html', {
                'profissional_list': profissional_list,
                })


def protocolo(request, ine, cns):
    profissional_filter = Profissional.objects.get(cns=cns)
    return render(request, 'core/ficha_protocolo.html', {
                'profissional_filter': profissional_filter,
                'linha': range(0, 56)
                })
