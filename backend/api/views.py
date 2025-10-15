"""ViewSets responsáveis por expor os recursos da aplicação."""

from rest_framework import viewsets

from .models import (
    DimCargo,
    DimLocalAtividade,
    DimRegimeTrabalho,
    DimRisk,
    DimTipoRequerimento,
    DimUO,
    DimUser,
    FactRequerimento,
)
from .serializers import (
    DimCargoSerializer,
    DimLocalAtividadeSerializer,
    DimRegimeTrabalhoSerializer,
    DimRiskSerializer,
    DimTipoRequerimentoSerializer,
    DimUOSerializer,
    DimUserSerializer,
    FactRequerimentoSerializer,
)


# =================================================================
# VIEWSETS DAS DIMENSÕES (CRUD de Tabelas de Lookup)
# =================================================================


class DimUserViewSet(viewsets.ModelViewSet):
    """CRUD para a tabela DimUser."""

    queryset = DimUser.objects.all()
    serializer_class = DimUserSerializer


class DimUOViewSet(viewsets.ModelViewSet):
    """CRUD para a tabela DimUO."""

    queryset = DimUO.objects.all()
    serializer_class = DimUOSerializer


class DimCargoViewSet(viewsets.ModelViewSet):
    """CRUD para a tabela DimCargo."""

    queryset = DimCargo.objects.all()
    serializer_class = DimCargoSerializer


class DimLocalAtividadeViewSet(viewsets.ModelViewSet):
    """CRUD para a tabela DimLocalAtividade."""

    queryset = DimLocalAtividade.objects.all()
    serializer_class = DimLocalAtividadeSerializer


class DimRegimeTrabalhoViewSet(viewsets.ModelViewSet):
    """CRUD para a tabela DimRegimeTrabalho."""

    queryset = DimRegimeTrabalho.objects.all()
    serializer_class = DimRegimeTrabalhoSerializer


class DimTipoRequerimentoViewSet(viewsets.ModelViewSet):
    """CRUD para a tabela DimTipoRequerimento."""

    queryset = DimTipoRequerimento.objects.all()
    serializer_class = DimTipoRequerimentoSerializer


class DimRiskViewSet(viewsets.ModelViewSet):
    """CRUD para a tabela DimRisk."""

    queryset = DimRisk.objects.all()
    serializer_class = DimRiskSerializer


# =================================================================
# VIEWSET DA TABELA FATO (FactRequerimento)
# =================================================================


class FactRequerimentoViewSet(viewsets.ModelViewSet):
    """CRUD e gestão da tabela de Fato (Requerimento)."""

    queryset = (
        FactRequerimento.objects.all()
        .select_related(
            "requerente",
            "funcionario",
            "uo",
            "regime_trabalho",
            "local_atividade",
            "tipo_requerimento",
        )
        .prefetch_related("riscos")
    )
    serializer_class = FactRequerimentoSerializer
