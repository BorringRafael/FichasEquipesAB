from django.contrib import admin
from .models import Unidade, Equipe, Profissional, CBO

admin.site.site_title = 'Fichas Profissionais AB'
admin.site.site_header = 'Fichas Profissionais AB'
admin.site.index_title = 'Fichas'
admin.site.register(Unidade),
admin.site.register(Equipe),
admin.site.register(Profissional),
admin.site.register(CBO),
