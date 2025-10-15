"""Initial schema for the api application."""

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DimCargo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=100)),
            ],
            options={"db_table": "dim_cargo", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="DimLocalAtividade",
            fields=[
                ("codigo", models.CharField(max_length=10, primary_key=True, serialize=False)),
                ("descricao", models.CharField(max_length=100)),
            ],
            options={"db_table": "dim_local_atividade", "ordering": ["descricao"]},
        ),
        migrations.CreateModel(
            name="DimRegimeTrabalho",
            fields=[
                ("codigo", models.CharField(max_length=10, primary_key=True, serialize=False)),
                ("descricao", models.CharField(max_length=100)),
            ],
            options={"db_table": "dim_regime_trabalho", "ordering": ["descricao"]},
        ),
        migrations.CreateModel(
            name="DimTipoRequerimento",
            fields=[
                ("codigo", models.CharField(max_length=10, primary_key=True, serialize=False)),
                ("descricao", models.CharField(max_length=100)),
            ],
            options={"db_table": "dim_tipo_requerimento", "ordering": ["descricao"]},
        ),
        migrations.CreateModel(
            name="DimUO",
            fields=[
                ("codigo", models.CharField(max_length=10, primary_key=True, serialize=False)),
                ("descricao", models.CharField(max_length=100)),
            ],
            options={"db_table": "dim_uo", "ordering": ["descricao"]},
        ),
        migrations.CreateModel(
            name="DimUser",
            fields=[
                ("matricula", models.CharField(max_length=20, primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=100)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("funcao", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={"db_table": "dim_user", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="DimRisk",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("codigo", models.CharField(max_length=50)),
                ("categoria", models.CharField(max_length=120)),
                ("subcategoria", models.CharField(max_length=120)),
                ("descricao", models.CharField(max_length=400)),
            ],
            options={
                "db_table": "dim_risk",
                "ordering": ["codigo", "subcategoria", "descricao"],
                "indexes": [
                    models.Index(fields=["codigo"], name="dim_risk_codigo_idx"),
                    models.Index(fields=["codigo", "subcategoria"], name="dim_risk_codigo_subcategoria_idx"),
                ],
                "unique_together": {("codigo", "subcategoria", "descricao")},
            },
        ),
        migrations.CreateModel(
            name="FactRequerimento",
            fields=[
                ("req_num", models.AutoField(primary_key=True, serialize=False)),
                ("status", models.CharField(max_length=50)),
                ("data_inicio", models.DateField(blank=True, null=True)),
                ("data_fim", models.DateField(blank=True, null=True)),
                (
                    "atividades_executadas",
                    models.TextField(
                        blank=True,
                        help_text="Descrição resumida das atividades executadas no requerimento.",
                    ),
                ),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
                ("data_processamento", models.DateTimeField(blank=True, null=True)),
                ("data_aprovacao", models.DateTimeField(blank=True, null=True)),
                ("doc_uuid", models.CharField(max_length=100, unique=True)),
                (
                    "funcionario",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="requerimentos_funcionarios",
                        to="api.dimuser",
                    ),
                ),
                (
                    "local_atividade",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="requerimentos_por_local",
                        to="api.dimlocalatividade",
                    ),
                ),
                (
                    "requerente",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="requerimentos_criados",
                        to="api.dimuser",
                    ),
                ),
                (
                    "regime_trabalho",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="requerimentos_por_regime",
                        to="api.dimregimetrabalho",
                    ),
                ),
                (
                    "tipo_requerimento",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="requerimentos_por_tipo",
                        to="api.dimtiporequerimento",
                    ),
                ),
                (
                    "uo",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        to="api.dimuo",
                    ),
                ),
            ],
            options={"db_table": "fato_requerimento", "ordering": ["-data_criacao"]},
        ),
        migrations.AddField(
            model_name="factrequerimento",
            name="riscos",
            field=models.ManyToManyField(
                blank=True,
                related_name="requerimentos_riscos",
                to="api.dimrisk",
            ),
        ),
    ]
