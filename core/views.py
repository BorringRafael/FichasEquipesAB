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


def lista_ficha_esus(request, v1, v2, v3):
    cbo = {
           'acs': '515105',
           'aux_enfermagem': '322250',
           'aux_saude_bucal': '322430',
           'dentista': '223293',
           'enfermeiro': '223565',
           'medico': '225142',
           'tec_enfermagem': '322245',
           'ass_social': '251605',
           'nutricionista': '223710',
           'psicologo': '251510',
           'fisioterapeuta': '223605',
           'educador_fisico': '22410',
           }
    nivel_superior = [
                      cbo['enfermeiro'],
                      cbo['medico'],
                      cbo['ass_social'],
                      cbo['nutricionista'],
                      cbo['fisioterapeuta'],
                      cbo['educador_fisico'],
                      ]
    nivel_medio = [
                   cbo['acs'],
                   cbo['aux_enfermagem'],
                   cbo['aux_saude_bucal'],
                   cbo['tec_enfermagem'],
                   ]
    profissional_filter = Profissional.objects.get(cns=v3)
    return render(request, 'core/ficha_esus.html', {
                'profissional_filter': profissional_filter,
                'pro_cbo': profissional_filter.cbo.cbo,
                'cbo': cbo,
                'nivel_superior': nivel_superior,
                'nivel_medio': nivel_medio,
                })


def ficha_esus(request, v1, v2, v3, v4):
    profissional_list = Profissional.objects.filter(equipe__ine=v2)
    profissional_filter = Profissional.objects.get(cns=v3)
    if v4 == 'ficha_atendimento_individual':
        return render(request, 'core/ficha_atendimento_individual.html', {
                    'profissional_filter': profissional_filter,
                    })
    elif v4 == 'ficha_atividade':
        return render(request, 'core/ficha_atividade.html', {
                    'profissional_filter': profissional_filter,
                    })
    elif v4 == 'ficha_cadastro_domiciliar':
        return render(request, 'core/ficha_cadastro_domiciliar.html', {
                    'profissional_filter': profissional_filter,
                    })
    elif v4 == 'ficha_cadastro_individual':
        return render(request, 'core/ficha_cadastro_individual.html', {
                    'profissional_filter': profissional_filter,
                    })
    elif v4 == 'ficha_de_procedimentos':
        return render(request, 'core/ficha_de_procedimentos.html', {
                    'profissional_filter': profissional_filter,
                    })
    elif v4 == 'ficha_de_visitas_domiciliar':
        return render(request, 'core/ficha_de_visitas_domiciliar.html', {
                    'profissional_filter': profissional_filter,
                    })
    elif v4 == 'ficha_individual_odontologico':
        return render(request, 'core/ficha_individual_odontologico.html', {
                    'profissional_filter': profissional_filter,
                    'profissional_list': profissional_list,
                    })
