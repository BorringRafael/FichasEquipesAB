from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles.finders import find

from .models import Equipe, Profissional, Auth_CBO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import white, black, red


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
        pdf.drawImage(find('core/img/Ficha_de_Atividade_Coletiva-0.png'),
                      0, 0, 21*cm, 29.7*cm)
        pdf.setFillColor(white)
        pdf.rect(10.45*cm, 21.4*cm, 9.83*cm, 3.5*cm, stroke=False,
                 fill=True)
        alt = 24.7*cm
        for value in Profissional.objects.filter(equipe__ine=v2).order_by('nome'):
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            pdf.drawString(12.4*cm, alt, value.nome)
            pdf.drawString(10.6*cm, alt, value.cns)
            pdf.drawString(17*cm, alt, value.cbo.cbo)
            pdf.drawString(17.7*cm, alt, value.cbo.nome)
            alt -= 6.0
        pdf.showPage()
        pdf.drawImage(find('core/img/Ficha_de_Atividade_Coletiva-1.png'),
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
                          find('core/img/Ficha_de_Atendimento_Individual-0.png'),
                          0, 0, 21*cm, 29.7*cm)
            """Retangulo"""
            pdf.setFillColor(white)
            """CNS"""
            pdf.rect(0.8*cm, 25.71*cm, 6*cm, 0.85*cm, stroke=False, fill=True)
            """CBO"""
            pdf.rect(6.99*cm, 25.71*cm, 2.9*cm, 0.85*cm, stroke=False,
                     fill=True)
            """CNES"""
            pdf.rect(10.1*cm, 25.71*cm, 2.9*cm, 0.85*cm, stroke=False,
                     fill=True)
            """INE"""
            pdf.rect(13.15*cm, 25.71*cm, 4.1*cm, 0.85*cm, stroke=False, fill=True)
            """Dados"""
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            """Nome Profissional"""
            pdf.drawString(0.8*cm, 26.4*cm, profissional_filter.nome)
            """Nome CBO"""
            pdf.drawString(6.95*cm, 26.4*cm, profissional_filter.cbo.nome)
            """Nome CNES"""
            pdf.drawString(10.1*cm, 26.4*cm,
                           profissional_filter.equipe.unidade.nome)
            """Número equipe"""
            if profissional_filter.equipe.area:
                pdf.drawString(13.15*cm, 26.4*cm, 'EQUIPE %s' % (profissional_filter.equipe.area))
            else:
                pdf.drawString(13.15*cm, 26.4*cm, 'NASF')
            pdf.setFontSize(0.5*cm)
            """CNES"""
            pdf.drawString(0.8*cm, 25.71*cm, profissional_filter.cns)
            """CBO"""
            pdf.drawString(6.95*cm, 25.71*cm, profissional_filter.cbo.cbo)
            """CNES"""
            pdf.drawString(10.1*cm, 25.71*cm,
                           profissional_filter.equipe.unidade.cnes)
            """INE"""
            pdf.drawString(13.15*cm, 25.71*cm, profissional_filter.equipe.ine)
            pdf.showPage()
            pdf.drawImage(
                          find('core/img/Ficha_de_Atendimento_Individual-1.png'),
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
            pdf.drawImage(find('core/img/Ficha_de_Atividade_Coletiva-0.png'),
                          0, 0, 21*cm, 29.7*cm)
            """Retangulo"""
            pdf.setFillColor(white)
            """CNS"""
            pdf.rect(0.85*cm, 25.85*cm, 5.75*cm, 0.75*cm, stroke=False, fill=True)
            """CBO"""
            pdf.rect(6.8*cm, 25.85*cm, 3*cm, 0.75*cm, stroke=False,
                     fill=True)
            """CNES"""
            pdf.rect(10.2*cm, 25.85*cm, 3*cm, 0.75*cm, stroke=False,
                     fill=True)
            """INE"""
            pdf.rect(13.5*cm, 25.85*cm, 4.1*cm, 0.75*cm, stroke=False, fill=True)
            """Dados"""
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            """Nome Profissional"""
            pdf.drawString(0.85*cm, 26.45*cm, profissional_filter.nome)
            """Nome CBO"""
            pdf.drawString(6.8*cm, 26.45*cm, profissional_filter.cbo.nome)
            """Nome CNES"""
            pdf.drawString(10.2*cm, 26.45*cm,
                           profissional_filter.equipe.unidade.nome)
            """Número equipe"""
            if profissional_filter.equipe.area:
                pdf.drawString(13.5*cm, 26.45*cm, 'EQUIPE %s' % (profissional_filter.equipe.area))
            else:
                pdf.drawString(13.5*cm, 26.45*cm, 'NASF')
            pdf.setFontSize(0.5*cm)
            """CNES"""
            pdf.drawString(0.85*cm, 25.85*cm, profissional_filter.cns)
            """CBO"""
            pdf.drawString(6.8*cm, 25.85*cm, profissional_filter.cbo.cbo)
            """CNES"""
            pdf.drawString(10.2*cm, 25.85*cm,
                           profissional_filter.equipe.unidade.cnes)
            """INE"""
            pdf.drawString(13.5*cm, 25.85*cm, profissional_filter.equipe.ine)
            pdf.setFillColor(white)
            pdf.rect(10.45*cm, 21.4*cm, 9.83*cm, 3.5*cm, stroke=False,
                     fill=True)
            alt = 24.7*cm
            for value in Profissional.objects.filter(equipe__ine=v2).order_by('nome'):
                pdf.setFillColor(black)
                pdf.setFontSize(0.2*cm)
                pdf.drawString(12.4*cm, alt, value.nome)
                pdf.drawString(10.6*cm, alt, value.cns)
                pdf.drawString(17*cm, alt, value.cbo.cbo)
                pdf.setFontSize(0.15*cm)
                pdf.drawString(17.7*cm, alt, value.cbo.nome)
                alt -= 6.0
            pdf.showPage()
            pdf.drawImage(find('core/img/Ficha_de_Atividade_Coletiva-1.png'),
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
                          find('core/img/Ficha_de_Procedimentos-0.png'),
                          0, 0, 21*cm, 29.7*cm)
            """Retangulo"""
            pdf.setFillColor(white)
            """CNS"""
            pdf.rect(0.88*cm, 25.8*cm, 5.9*cm, 0.9*cm, stroke=False, fill=True)
            """CBO"""
            pdf.rect(6.99*cm, 25.8*cm, 2.9*cm, 0.9*cm, stroke=False,
                     fill=True)
            """CNES"""
            pdf.rect(10.1*cm, 25.8*cm, 2.9*cm, 0.9*cm, stroke=False,
                     fill=True)
            """INE"""
            pdf.rect(13.2*cm, 25.8*cm, 4*cm, 0.9*cm, stroke=False, fill=True)
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            """Nome Profissional"""
            pdf.drawString(0.88*cm, 26.5*cm, profissional_filter.nome)
            """Nome CBO"""
            pdf.drawString(6.99*cm, 26.5*cm, profissional_filter.cbo.nome)
            """Nome CNES"""
            pdf.drawString(10.1*cm, 26.5*cm,
                           profissional_filter.equipe.unidade.nome)
            """Nome INE"""
            pdf.drawString(13.2*cm, 26.5*cm, 'EQUIPE %s' % profissional_filter.equipe.area)
            pdf.setFontSize(0.5*cm)
            """CNS"""
            pdf.drawString(0.88*cm, 25.8*cm, profissional_filter.cns)
            """CBO"""
            pdf.drawString(6.99*cm, 25.8*cm, profissional_filter.cbo.cbo)
            """CNES"""
            pdf.drawString(10.1*cm, 25.8*cm,
                           profissional_filter.equipe.unidade.cnes)
            """INE"""
            pdf.drawString(13.2*cm, 25.8*cm, profissional_filter.equipe.ine)
            pdf.showPage()
            pdf.drawImage(
                          find('core/img/Ficha_de_Procedimentos-1.png'),
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
                          find('core/img/Ficha_de_Visita_Domiciliar_e_Territorial-0.png'),
                          0, 0, 29.7*cm, 21*cm)
            """Retangulo"""
            pdf.setFillColor(white)
            """CNS"""
            pdf.rect(1.1*cm, 17.05*cm, 8*cm, 0.9*cm, stroke=False, fill=True)
            """CBO"""
            pdf.rect(9.5*cm, 17.05*cm, 4.4*cm, 0.9*cm, stroke=False,
                     fill=True)
            """CNES"""
            pdf.rect(14.3*cm, 17.05*cm, 4.5*cm, 0.9*cm, stroke=False,
                     fill=True)
            """INE"""
            pdf.rect(19.2*cm, 17.05*cm, 5*cm, 0.9*cm, stroke=False, fill=True)
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            """Nome Profissional"""
            pdf.drawString(1.1*cm, 17.7*cm, profissional_filter.nome)
            """Nome CBO"""
            pdf.drawString(9.5*cm, 17.7*cm, profissional_filter.cbo.nome)
            """Nome CNES"""
            pdf.drawString(14.3*cm, 17.7*cm,
                           profissional_filter.equipe.unidade.nome)
            """Nome INE"""
            pdf.drawString(19.2*cm, 17.7*cm, 'EQUIPE %s' % profissional_filter.equipe.area)
            pdf.setFontSize(0.5*cm)
            """CNS"""
            pdf.drawString(1.1*cm, 17.05*cm, profissional_filter.cns)
            """CBO"""
            pdf.drawString(9.5*cm, 17.05*cm, profissional_filter.cbo.cbo)
            """CNES"""
            pdf.drawString(14.3*cm, 17.05*cm,
                           profissional_filter.equipe.unidade.cnes)
            """INE"""
            pdf.drawString(19.2*cm, 17.05*cm, profissional_filter.equipe.ine)
            pdf.showPage()
            pdf.drawImage(
                          find('core/img/Ficha_de_Visita_Domiciliar_e_Territorial-1.png'),
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
                          find('core/img/Ficha_de_Atendimento_Odontologico_Individual-0.png'),
                          0, 0, 21*cm, 29.7*cm)
            """Retangulo"""
            pdf.setFillColor(white)
            """CNS"""
            pdf.rect(0.8*cm, 25.71*cm, 6*cm, 0.85*cm, stroke=False, fill=True)
            """CBO"""
            pdf.rect(6.99*cm, 25.71*cm, 2.9*cm, 0.85*cm, stroke=False,
                     fill=True)
            """CNES"""
            pdf.rect(10.1*cm, 25.71*cm, 2.9*cm, 0.85*cm, stroke=False,
                     fill=True)
            """INE"""
            pdf.rect(13.15*cm, 25.71*cm, 4.1*cm, 0.85*cm, stroke=False, fill=True)
            """Dados"""
            pdf.setFillColor(black)
            pdf.setFontSize(0.2*cm)
            """Nome Profissional"""
            pdf.drawString(0.8*cm, 26.4*cm, profissional_filter.nome)
            """Nome CBO"""
            pdf.drawString(6.95*cm, 26.4*cm, profissional_filter.cbo.nome)
            """Nome CNES"""
            pdf.drawString(10.1*cm, 26.4*cm,
                           profissional_filter.equipe.unidade.nome)
            """Número equipe"""
            if profissional_filter.equipe.area:
                pdf.drawString(13.15*cm, 26.4*cm, 'EQUIPE %s' % (profissional_filter.equipe.area))
            else:
                pdf.drawString(13.15*cm, 26.4*cm, 'NASF')
            pdf.setFontSize(0.5*cm)
            """CNES"""
            pdf.drawString(0.8*cm, 25.71*cm, profissional_filter.cns)
            """CBO"""
            pdf.drawString(6.95*cm, 25.71*cm, profissional_filter.cbo.cbo)
            """CNES"""
            pdf.drawString(10.1*cm, 25.71*cm,
                           profissional_filter.equipe.unidade.cnes)
            """INE"""
            pdf.drawString(13.15*cm, 25.71*cm, profissional_filter.equipe.ine)
            for value in profissional_list:
                if value.cbo.cbo == '322430':
                    """Retangulo"""
                    pdf.setFillColor(white)
                    """CNS"""
                    pdf.rect(0.8*cm, 24.71*cm, 6*cm, 0.85*cm, stroke=False, fill=True)
                    """CBO"""
                    pdf.rect(6.99*cm, 24.71*cm, 2.9*cm, 0.85*cm, stroke=False,
                             fill=True)
                    """CNES"""
                    pdf.rect(10.1*cm, 24.71*cm, 2.9*cm, 0.85*cm, stroke=False,
                             fill=True)
                    """INE"""
                    pdf.rect(13.15*cm, 24.71*cm, 4.1*cm, 0.85*cm, stroke=False, fill=True)
                    """Dados"""
                    pdf.setFillColor(black)
                    pdf.setFontSize(0.2*cm)
                    """Nome Profissional"""
                    pdf.drawString(0.8*cm, 25.4*cm, value.nome)
                    """Nome CBO"""
                    pdf.drawString(6.95*cm, 25.4*cm, value.cbo.nome)
                    """Nome CNES"""
                    pdf.drawString(10.1*cm, 25.4*cm,
                                   value.equipe.unidade.nome)
                    """Número equipe"""
                    if profissional_filter.equipe.area:
                        pdf.drawString(13.15*cm, 25.4*cm, 'EQUIPE %s' % (value.equipe.area))
                    else:
                        pdf.drawString(13.15*cm, 25.4*cm, 'NASF')
                    pdf.setFontSize(0.5*cm)
                    """CNES"""
                    pdf.drawString(0.8*cm, 24.71*cm, value.cns)
                    """CBO"""
                    pdf.drawString(6.95*cm, 24.71*cm, value.cbo.cbo)
                    """CNES"""
                    pdf.drawString(10.1*cm, 24.71*cm,
                                   value.equipe.unidade.cnes)
                    """INE"""
                    pdf.drawString(13.15*cm, 24.71*cm, value.equipe.ine)
            pdf.showPage()
            pdf.drawImage(
                          find('core/img/Ficha_de_Atendimento_Odontologico_Individual-1.png'),
                          0, 0, 21*cm, 29.7*cm)
            pdf.showPage()
            pdf.save()
            return response
        else:
            return HttpResponse(message)
