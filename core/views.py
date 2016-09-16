from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles.finders import find

from .models import Equipe, Profissional, Auth_CBO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import white, black


def equipe(request, v1):
    '''Listar Equipes'''
    equipe_list = Equipe.objects.all()
    return render(request, 'core/equipe.html', {
                'equipe_list': equipe_list,
                'v1': v1,
                })


def profissional(request, v1, v2):
    '''Listar Profissionais'''
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
    '''Ficha de Protocolo'''
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


def ficha_atividade(request, v1, v2):
    '''Ficha de Atividade Coletiva da Equipe'''
    message = 'Ficha usada apenas pelas equipes PSF'
    if Equipe.objects.filter(ine=v2).exists():
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline;\
            filename="%s_ficha_atividade.pdf"' % v2
        pdf = canvas.Canvas(response, pagesize=A4)
        pdf.drawImage(find('core/img/ficha_atividade-0.png'),
                      0, 0, 21*cm, 29.7*cm)
        pdf.setFillColor(white)
        pdf.rect(8.699*cm, 22.35*cm, 7.31*cm, 3.55*cm, stroke=False,
                 fill=True)
        pdf.rect(16.03*cm, 22.35*cm, 4.39*cm, 3.55*cm, stroke=False,
                 fill=True)
        pdf.rect(0.7*cm, 1.1*cm, 5.3*cm, 0.45*cm, stroke=False, fill=True)
        pdf.rect(6.2*cm, 1.1*cm, 2.5*cm, 0.45*cm, stroke=False, fill=True)
        pdf.rect(8.85*cm, 1.1*cm, 3.6*cm, 0.45*cm, stroke=False, fill=True)
        alt = 25.7*cm
        for profissional_filter in Profissional.objects.filter(equipe__ine=v2):
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            pdf.drawString(10.6*cm, alt, profissional_filter.nome)
            pdf.drawString(8.8*cm, alt, profissional_filter.cns)
            pdf.drawString(16.2*cm, alt, profissional_filter.cbo.cbo)
            alt -= 6.0
        pdf.showPage()
        pdf.drawImage(find('core/img/ficha_atividade-1.png'),
                      0, 0, 21*cm, 29.7*cm)
        pdf.showPage()
        pdf.save()
        return response
    else:
        return HttpResponse(message)


def lista_ficha_esus(request, v1, v2, v3):
    '''Listar Fichas e-SUS-AB'''
    profissional_filter = Profissional.objects.get(cns=v3)
    auth_cbo = Auth_CBO.objects.all()
    return render(request, 'core/ficha_esus.html', {
                'profissional_filter': profissional_filter,
                'pro_cbo': profissional_filter.cbo.cbo,
                'auth_cbo': auth_cbo,
                })


def ficha_esus(request, v1, v2, v3, v4):
    '''Fichas e-SUS-AB'''
    profissional_list = Profissional.objects.filter(equipe__ine=v2)
    profissional_filter = Profissional.objects.get(cns=v3)
    auth_cbo = Auth_CBO.objects.all()
    message = 'Ficha não disponível para %s' % profissional_filter.cbo.nome
    if v4 == 'ficha_atendimento_individual':
        if auth_cbo.filter(
                           nome=v4,
                           cbo__cbo=profissional_filter.cbo.cbo,
                           ).exists():
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline;\
                filename="%s_ficha_atendimento_individual.pdf"'\
                % profissional_filter.nome
            pdf = canvas.Canvas(response, pagesize=A4)
            pdf.drawImage(
                          find('core/img/ficha_atendimento_individual-0.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.setFillColor(white)
            pdf.rect(0.8*cm, 25.71*cm, 6*cm, 0.9*cm, stroke=False, fill=True)
            pdf.rect(6.95*cm, 25.71*cm, 2.75*cm, 0.4*cm, stroke=False,
                     fill=True)
            pdf.rect(9.9*cm, 25.71*cm, 2.75*cm, 0.4*cm, stroke=False,
                     fill=True)
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
        else:
            return HttpResponse(message)
    elif v4 == 'ficha_atividade':
        if auth_cbo.filter(
                           nome=v4,
                           cbo__cbo=profissional_filter.cbo.cbo,
                           ).exists():
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline;\
                filename="%s_ficha_atividade.pdf"' % profissional_filter.nome
            pdf = canvas.Canvas(response, pagesize=A4)
            pdf.drawImage(find('core/img/ficha_atividade-0.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.setFillColor(white)
            pdf.rect(8.699*cm, 22.35*cm, 7.31*cm, 3.55*cm, stroke=False,
                     fill=True)
            pdf.rect(16.03*cm, 22.35*cm, 4.39*cm, 3.55*cm, stroke=False,
                     fill=True)
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
            pdf.drawString(6.2*cm, 1.1*cm,
                           profissional_filter.equipe.unidade.cnes)
            pdf.drawString(8.85*cm, 1.1*cm, profissional_filter.equipe.ine)
            pdf.showPage()
            pdf.drawImage(find('core/img/ficha_atividade-1.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.showPage()
            pdf.save()
            return response
        else:
            return HttpResponse(message)
    elif v4 == 'ficha_cadastro_domiciliar':
        if auth_cbo.filter(
                           nome=v4,
                           cbo__cbo=profissional_filter.cbo.cbo,
                           ).exists():
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline;\
                filename="%s_ficha_cadastro_domiciliar.pdf"'\
                % profissional_filter.nome
            pdf = canvas.Canvas(response, pagesize=A4)
            pdf.drawImage(find('core/img/ficha_cadastro_domiciliar.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.setFillColor(white)
            pdf.rect(0.8*cm, 25.5*cm, 6.7*cm, 0.9*cm, stroke=False, fill=True)
            pdf.rect(8*cm, 25.5*cm, 3*cm, 0.4*cm, stroke=False, fill=True)
            pdf.rect(11.55*cm, 25.5*cm, 3.8*cm, 0.4*cm, stroke=False,
                     fill=True)
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            pdf.drawString(0.8*cm, 26.1*cm, profissional_filter.nome)
            pdf.setFontSize(0.5*cm)
            pdf.drawString(0.8*cm, 25.5*cm, profissional_filter.cns)
            pdf.drawString(8*cm, 25.5*cm,
                           profissional_filter.equipe.unidade.cnes)
            pdf.drawString(11.55*cm, 25.5*cm, profissional_filter.equipe.ine)
            pdf.showPage()
            pdf.save()
            return response
        else:
            return HttpResponse(message)
    elif v4 == 'ficha_cadastro_individual':
        if auth_cbo.filter(
                           nome=v4,
                           cbo__cbo=profissional_filter.cbo.cbo,
                           ).exists():
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline;\
                filename="%s_ficha_cadastro_individual.pdf"'\
                % profissional_filter.nome
            pdf = canvas.Canvas(response, pagesize=A4)
            pdf.drawImage(find('core/img/ficha_cadastro_individual-0.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.setFillColor(white)
            pdf.rect(0.8*cm, 26.25*cm, 6.7*cm, 0.9*cm, stroke=False, fill=True)
            pdf.rect(8*cm, 26.25*cm, 3.1*cm, 0.4*cm, stroke=False, fill=True)
            pdf.rect(11.55*cm, 26.25*cm, 3.8*cm, 0.4*cm, stroke=False,
                     fill=True)
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            pdf.drawString(0.8*cm, 26.9*cm, profissional_filter.nome)
            pdf.setFontSize(0.5*cm)
            pdf.drawString(0.8*cm, 26.25*cm, profissional_filter.cns)
            pdf.drawString(8*cm, 26.25*cm,
                           profissional_filter.equipe.unidade.cnes)
            pdf.drawString(11.55*cm, 26.25*cm, profissional_filter.equipe.ine)
            pdf.showPage()
            pdf.drawImage(find('core/img/ficha_cadastro_individual-1.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.showPage()
            pdf.save()
            return response
        else:
            return HttpResponse(message)
    elif v4 == 'ficha_de_procedimentos':
        if auth_cbo.filter(
                           nome=v4,
                           cbo__cbo=profissional_filter.cbo.cbo,
                           ).exists():
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline;\
                filename="%s_ficha_de_procedimentos.pdf"'\
                % profissional_filter.nome
            pdf = canvas.Canvas(response, pagesize=A4)
            pdf.drawImage(
                          find('core/img/ficha_de_procedimentos-0.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.setFillColor(white)
            pdf.rect(0.8*cm, 25.77*cm, 6.2*cm, 0.9*cm, stroke=False, fill=True)
            pdf.rect(7.25*cm, 25.77*cm, 2.9*cm, 0.4*cm, stroke=False,
                     fill=True)
            pdf.rect(10.3*cm, 25.77*cm, 3*cm, 0.4*cm, stroke=False, fill=True)
            pdf.rect(13.55*cm, 25.77*cm, 4.3*cm, 0.4*cm, stroke=False,
                     fill=True)
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            pdf.drawString(0.8*cm, 26.45*cm, profissional_filter.nome)
            pdf.setFontSize(0.5*cm)
            pdf.drawString(0.8*cm, 25.8*cm, profissional_filter.cns)
            pdf.drawString(7.25*cm, 25.8*cm, profissional_filter.cbo.cbo)
            pdf.drawString(10.3*cm, 25.8*cm,
                           profissional_filter.equipe.unidade.cnes)
            pdf.drawString(13.55*cm, 25.8*cm, profissional_filter.equipe.ine)
            pdf.showPage()
            pdf.drawImage(
                          find('core/img/ficha_de_procedimentos-1.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.showPage()
            pdf.save()
            return response
    elif v4 == 'ficha_de_visitas_domiciliar':
        if auth_cbo.filter(
                           nome=v4,
                           cbo__cbo=profissional_filter.cbo.cbo,
                           ).exists():
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline;\
                filename="%s_ficha_de_visitas_domiciliar.pdf"'\
                % profissional_filter.nome
            pdf = canvas.Canvas(response, pagesize=landscape(A4))
            pdf.drawImage(
                          find('core/img/ficha_de_visitas_domiciliar-0.png'),
                          0, 0, 29.7*cm, 21*cm)
            pdf.setFillColor(white)
            pdf.rect(0.85*cm, 17.05*cm, 6.2*cm, 0.85*cm, stroke=False,
                     fill=True)
            pdf.rect(7.3*cm, 17.05*cm, 5.2*cm, 0.4*cm, stroke=False, fill=True)
            pdf.rect(13*cm, 17.05*cm, 4.2*cm, 0.4*cm, stroke=False, fill=True)
            pdf.rect(18.8*cm, 17.05*cm, 4.2*cm, 0.4*cm, stroke=False,
                     fill=True)
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            pdf.drawString(0.85*cm, 17.7*cm, profissional_filter.nome)
            pdf.setFontSize(0.5*cm)
            pdf.drawString(0.85*cm, 17.05*cm, profissional_filter.cns)
            pdf.drawString(7.3*cm, 17.05*cm, profissional_filter.cbo.cbo)
            pdf.drawString(13*cm, 17.05*cm,
                           profissional_filter.equipe.unidade.cnes)
            pdf.drawString(18.8*cm, 17.05*cm, profissional_filter.equipe.ine)
            pdf.showPage()
            pdf.drawImage(
                          find('core/img/ficha_de_visitas_domiciliar-1.png'),
                          0, 0, 29.7*cm, 21*cm)
            pdf.showPage()
            pdf.save()
            return response
        else:
            return HttpResponse(message)
    elif v4 == 'ficha_individual_odontologico':
        if auth_cbo.filter(
                           nome=v4,
                           cbo__cbo=profissional_filter.cbo.cbo,
                           ).exists():
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline;\
                filename="%s_ficha_individual_odontologico.pdf"'\
                % profissional_filter.nome
            pdf = canvas.Canvas(response, pagesize=A4)
            pdf.drawImage(
                          find('core/img/ficha_individual_odontologico-0.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.setFillColor(white)
            pdf.rect(0.8*cm, 25.71*cm, 6*cm, 0.9*cm, stroke=False, fill=True)
            pdf.rect(6.95*cm, 25.71*cm, 2.75*cm, 0.4*cm, stroke=False,
                     fill=True)
            pdf.rect(10*cm, 25.71*cm, 4*cm, 0.4*cm, stroke=False, fill=True)
            pdf.rect(14.25*cm, 25.71*cm, 2.6*cm, 0.4*cm, stroke=False,
                     fill=True)
            pdf.rect(0.8*cm, 24.71*cm, 6*cm, 0.9*cm, stroke=False, fill=True)
            pdf.rect(6.95*cm, 24.71*cm, 2.75*cm, 0.4*cm, stroke=False,
                     fill=True)
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            pdf.drawString(0.8*cm, 26.4*cm, profissional_filter.nome)
            pdf.setFontSize(0.5*cm)
            pdf.drawString(0.8*cm, 25.71*cm, profissional_filter.cns)
            pdf.drawString(6.95*cm, 25.71*cm,
                           profissional_filter.equipe.unidade.cnes)
            pdf.drawString(10*cm, 25.71*cm, profissional_filter.equipe.ine)
            pdf.drawString(14.25*cm, 25.71*cm, profissional_filter.cbo.cbo)
            for value in profissional_list:
                if value.cbo.cbo == '322430':
                    pdf.setFontSize(0.2*cm)
                    pdf.drawString(0.8*cm, 25.4*cm, value.nome)
                    pdf.setFontSize(0.5*cm)
                    pdf.drawString(0.8*cm, 24.71*cm, value.cns)
                    pdf.drawString(6.95*cm, 24.71*cm, value.cbo.cbo)
            pdf.showPage()
            pdf.drawImage(
                          find('core/img/ficha_individual_odontologico-1.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.showPage()
            pdf.save()
            return response
        else:
            return HttpResponse(message)
