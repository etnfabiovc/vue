"""Signals responsáveis por manter tabelas de dimensão sincronizadas com os arquivos base."""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Dict, Iterable

from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import DimRisk, DimUO, DimUser

logger = logging.getLogger(__name__)

DATA_DIR = Path(settings.BASE_DIR).parent / "frontend" / "src" / "assets" / "files"


def _normalize_key(value: str | None) -> str:
    if not value:
        return ""
    return value.replace("\ufeff", "").strip()


def _normalize_value(value: str | None) -> str:
    if value is None:
        return ""
    return value.replace("\ufeff", "").strip()


def _read_csv(filename: str) -> Iterable[Dict[str, str]]:
    csv_path = DATA_DIR / filename
    if not csv_path.exists():
        logger.warning("Arquivo de carga não encontrado: %s", csv_path)
        return []

    with csv_path.open(encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream, delimiter=";")
        for row in reader:
            normalized = {_normalize_key(key): _normalize_value(val) for key, val in row.items()}
            yield normalized


def _load_risks() -> None:
    rows = list(_read_csv("dimRisk.csv"))
    if not rows:
        return

    with transaction.atomic():
        for row in rows:
            codigo = row.get("codigo")
            subcategoria = row.get("subcategoria")
            descricao = row.get("descricao")
            categoria = row.get("categoria", "")

            if not codigo or not subcategoria or not descricao:
                continue

            DimRisk.objects.update_or_create(
                codigo=codigo,
                subcategoria=subcategoria,
                descricao=descricao,
                defaults={"categoria": categoria},
            )


def _load_users() -> None:
    rows = list(_read_csv("dimUser.csv"))
    if not rows:
        return

    with transaction.atomic():
        for row in rows:
            matricula = row.get("matricula")
            nome = row.get("nome")
            if not matricula or not nome:
                continue

            email = row.get("email") or None
            funcao = row.get("cargo") or None
            uo_code = row.get("uo") or ""

            uo_instance = None
            if uo_code:
                uo_instance, _ = DimUO.objects.get_or_create(
                    codigo=uo_code,
                    defaults={"descricao": uo_code},
                )

            DimUser.objects.update_or_create(
                matricula=matricula,
                defaults={
                    "nome": nome,
                    "email": email,
                    "funcao": funcao,
                    "uo": uo_instance,
                },
            )


@receiver(post_migrate)
def populate_dimensions(sender, **kwargs) -> None:
    if sender.name != "api":
        return

    try:
        _load_risks()
        _load_users()
    except Exception:  # pragma: no cover - apenas log de suporte
        logger.exception("Falha ao popular tabelas de dimensão")
