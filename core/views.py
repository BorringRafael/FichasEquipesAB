from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles.finders import find

from .models import Equipe, Profissional

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import white, black


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
    '''Capa das fichas de protocolo'''
    if Equipe.objects.filter(ine=v2).exists():
        equipe = Equipe.objects.get(ine=v2)
    else:
        equipe = Equipe.objects.get(nome=v2)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline;\
        filename="%s_capa_protocolo.pdf"' % equipe.nome
    pdf = canvas.Canvas(response, pagesize=A4)
    pdf.drawImage(find('core/img/capa_protocolo.png'), 0, 0, 21*cm, 29.7*cm)
    pdf.drawCentredString(10.5*cm, 2*cm, equipe.unidade.nome)
    pdf.drawString(2*cm, 1.1*cm, equipe.nome)
    pdf.drawString(11.1*cm, 1.1*cm, equipe.area)
    pdf.drawString(16.1*cm, 1.1*cm, equipe.ine)
    pdf.showPage()
    pdf.save()
    return response


def ficha_protocolo(request, v1, v2, v3):
    profissional_filter = Profissional.objects.get(cns=v3)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline;\
        filename="%s_ficha_protocolo.pdf"' % profissional_filter.nome
    pdf = canvas.Canvas(response, pagesize=A4)
    pdf.drawImage(find('core/img/ficha_protocolo-0.png'), 0, 0, 21*cm, 29.7*cm)
    pdf.drawString(2.1*cm, 25.75*cm, profissional_filter.equipe.nome)
    pdf.drawString(11.4*cm, 25.75*cm, profissional_filter.equipe.ine)
    pdf.drawString(16.8*cm, 25.75*cm, profissional_filter.equipe.unidade.cnes)
    pdf.drawString(2.9*cm, 24.85*cm, profissional_filter.nome)
    pdf.drawString(13.7*cm, 24.85*cm, profissional_filter.cns)
    pdf.showPage()
    pdf.drawImage(find('core/img/ficha_protocolo-1.png'), 0, 0, 21*cm, 29.7*cm)
    pdf.showPage()
    pdf.save()
    return response


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
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline;\
            filename="%s_ficha_protocolo.pdf"' % profissional_filter.nome
        pdf = canvas.Canvas(response, pagesize=A4)
        pdf.drawImage(
                      find('core/img/ficha_atendimento_individual-0.png'),
                      0, 0, 21*cm, 29.7*cm)
        pdf.setFillColor(white)
        pdf.rect(0.8*cm, 25.71*cm, 6*cm, 0.9*cm, stroke=False, fill=True)
        pdf.rect(6.95*cm, 25.71*cm, 2.75*cm, 0.4*cm, stroke=False, fill=True)
        pdf.rect(9.9*cm, 25.71*cm, 2.75*cm, 0.4*cm, stroke=False, fill=True)
        pdf.rect(12.8*cm, 25.71*cm, 4*cm, 0.4*cm, stroke=False, fill=True)
        pdf.setFillColor(black)
        pdf.setFontSize(0.2*cm)
        pdf.drawString(0.8*cm, 26.4*cm, profissional_filter.nome)
        pdf.setFontSize(0.5*cm)
        pdf.drawString(0.8*cm, 25.71*cm, profissional_filter.cns)
        pdf.drawString(6.95*cm, 25.71*cm, profissional_filter.cbo.cbo)
        pdf.drawString(9.9*cm, 25.71*cm,
                       profissional_filter.equipe.unidade.cnes)
        pdf.drawString(12.8*cm, 25.71*cm, profissional_filter.equipe.ine)
        pdf.showPage()
        pdf.drawImage(
                      find('core/img/ficha_atendimento_individual-1.png'),
                      0, 0, 21*cm, 29.7*cm)
        pdf.showPage()
        pdf.save()
        return response
    elif v4 == 'ficha_atividade':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline;\
            filename="%s_ficha_protocolo.pdf"' % profissional_filter.nome
        pdf = canvas.Canvas(response, pagesize=A4)
        pdf.drawImage(find('core/img/ficha_atividade-0.png'),
                      0, 0, 21*cm, 29.7*cm)
        pdf.setFillColor(white)
        pdf.rect(8.699*cm, 22.35*cm, 7.31*cm, 3.55*cm, stroke=False, fill=True)
        pdf.rect(16.03*cm, 22.35*cm, 4.39*cm, 3.55*cm, stroke=False, fill=True)
        pdf.rect(0.7*cm, 1.1*cm, 5.3*cm, 0.45*cm, stroke=False, fill=True)
        pdf.rect(6.2*cm, 1.1*cm, 2.5*cm, 0.45*cm, stroke=False, fill=True)
        pdf.rect(8.85*cm, 1.1*cm, 3.6*cm, 0.45*cm, stroke=False, fill=True)
        pdf.setFillColor(black)
        pdf.setFontSize(0.2*cm)
        pdf.drawString(10.6*cm, 25.7*cm, profissional_filter.nome)
        pdf.drawString(8.8*cm, 25.7*cm, profissional_filter.cns)
        pdf.drawString(16.2*cm, 25.7*cm, profissional_filter.cbo.cbo)
        pdf.drawString(0.7*cm, 1.6*cm, profissional_filter.nome)
        pdf.setFontSize(0.5*cm)
        pdf.drawString(0.7*cm, 1.1*cm, profissional_filter.cns)
        pdf.drawString(6.2*cm, 1.1*cm, profissional_filter.equipe.unidade.cnes)
        pdf.drawString(8.85*cm, 1.1*cm, profissional_filter.equipe.ine)
        pdf.showPage()
        pdf.drawImage(find('core/img/ficha_atividade-1.png'),
                      0, 0, 21*cm, 29.7*cm)
        pdf.showPage()
        pdf.save()
        return response
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
