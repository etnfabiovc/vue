"""Modelos das dimensões e da tabela fato utilizados pela API."""

from django.db import models


# === DIMENSÕES === #


class DimUser(models.Model):
    matricula = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    funcao = models.CharField(max_length=100, blank=True, null=True)
    uo = models.ForeignKey(
        "DimUO",
        on_delete=models.PROTECT,
        related_name="usuarios",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "dim_user"
        ordering = ["nome"]

    def __str__(self) -> str:  # pragma: no cover - representação amigável
        return f"{self.nome} ({self.matricula})"


class DimUO(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    descricao = models.CharField(max_length=100)

    class Meta:
        db_table = "dim_uo"
        ordering = ["descricao"]

    def __str__(self) -> str:  # pragma: no cover - representação amigável
        return self.descricao


class DimCargo(models.Model):
    """Dimensão responsável por armazenar os cargos cadastrados."""

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    class Meta:
        db_table = "dim_cargo"
        ordering = ["nome"]

    def __str__(self) -> str:  # pragma: no cover - representação amigável
        return self.nome


class DimLocalAtividade(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    descricao = models.CharField(max_length=100)

    class Meta:
        db_table = "dim_local_atividade"
        ordering = ["descricao"]

    def __str__(self) -> str:  # pragma: no cover - representação amigável
        return self.descricao


class DimTipoRequerimento(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    descricao = models.CharField(max_length=100)

    class Meta:
        db_table = "dim_tipo_requerimento"
        ordering = ["descricao"]

    def __str__(self) -> str:  # pragma: no cover - representação amigável
        return self.descricao


class DimRegimeTrabalho(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    descricao = models.CharField(max_length=100)

    class Meta:
        db_table = "dim_regime_trabalho"
        ordering = ["descricao"]

    def __str__(self) -> str:  # pragma: no cover - representação amigável
        return self.descricao


class DimRisk(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(max_length=50)
    categoria = models.CharField(max_length=120)
    subcategoria = models.CharField(max_length=120)
    descricao = models.CharField(max_length=400)

    class Meta:
        db_table = "dim_risk"
        indexes = [
            models.Index(fields=["codigo"]),
            models.Index(fields=["codigo", "subcategoria"]),
        ]
        unique_together = ("codigo", "subcategoria", "descricao")
        ordering = ["codigo", "subcategoria", "descricao"]

    def __str__(self) -> str:  # pragma: no cover - representação amigável
        return f"{self.codigo} • {self.subcategoria} • {self.descricao}"


# === TABELA FATO (FactRequerimento) === #


class FactRequerimento(models.Model):
    """Tabela fato que consolida os dados do processo de requerimento."""

    req_num = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    atividades_executadas = models.TextField(
        blank=True,
        help_text="Descrição resumida das atividades executadas no requerimento.",
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_processamento = models.DateTimeField(null=True, blank=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    doc_uuid = models.CharField(max_length=100, unique=True)

    # Chaves Estrangeiras (Dimensões)
    requerente = models.ForeignKey(
        DimUser,
        on_delete=models.PROTECT,
        related_name="requerimentos_criados",
    )
    funcionario = models.ForeignKey(
        DimUser,
        on_delete=models.PROTECT,
        related_name="requerimentos_funcionarios",
    )
    uo = models.ForeignKey(DimUO, on_delete=models.PROTECT)
    regime_trabalho = models.ForeignKey(
        DimRegimeTrabalho,
        on_delete=models.PROTECT,
        related_name="requerimentos_por_regime",
    )
    local_atividade = models.ForeignKey(
        DimLocalAtividade,
        on_delete=models.PROTECT,
        related_name="requerimentos_por_local",
    )
    tipo_requerimento = models.ForeignKey(
        DimTipoRequerimento,
        on_delete=models.PROTECT,
        related_name="requerimentos_por_tipo",
    )

    # Relação Muitos-Para-Muitos para Riscos (Degenerada)
    riscos = models.ManyToManyField(
        DimRisk,
        related_name="requerimentos_riscos",
        blank=True,
    )

    class Meta:
        db_table = "fato_requerimento"
        ordering = ["-data_criacao"]

    def __str__(self) -> str:  # pragma: no cover - representação amigável
        return f"Req {self.req_num} - {self.status}"
