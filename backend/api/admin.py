# admin.py (na pasta do seu app)

from django.contrib import admin
from .models import (
    DimUser, DimUO, DimCargo, DimLocalAtividade, DimRegimeTrabalho, 
    DimTipoRequerimento, DimRisk, FactRequerimento
)

# Registro de todas as dimensões
admin.site.register(DimUser)
admin.site.register(DimUO)
admin.site.register(DimCargo)
admin.site.register(DimLocalAtividade)
admin.site.register(DimRegimeTrabalho)
admin.site.register(DimTipoRequerimento)
admin.site.register(DimRisk)

# Registro da Tabela de Fato
admin.site.register(FactRequerimento)