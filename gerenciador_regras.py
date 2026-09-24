import json
import re
from pathlib import Path

from normalizador import normalizar_texto


def validar_regras(regras: list) -> bool:

    if not isinstance(regras, list):
        return False

    for regra in regras:

        if not isinstance(regra, dict):
            return False

        if "item" not in regra:
            return False

        if "fragmentos" not in regra:
            return False

        if not isinstance(regra["fragmentos"], list):
            return False

        if len(regra["fragmentos"]) == 0:
            return False

    return True


def preparar_regras(regras: list) -> list:

    regras_preparadas = []

    for regra in regras:

        fragmentos_preparados = []

        for fragmento in regra["fragmentos"]:

            fragmento_normalizado = normalizar_texto(fragmento)

            padrao = r"\b" + re.escape(fragmento_normalizado) + r"\b"

            fragmentos_preparados.append(padrao)

        regras_preparadas.append({
            "id": regra.get("id"),
            "item": regra["item"],
            "fragmentos": regra["fragmentos"],
            "criterio": regra.get("criterio", "qualquer"),
            "padroes": fragmentos_preparados
        })

    return regras_preparadas


def carregar_regras() -> list:

    base_dir = Path(__file__).resolve().parent
    caminho_regras = base_dir / "regras.json"

    with open(caminho_regras, "r", encoding="utf-8") as arquivo:
        regras = json.load(arquivo)

    if not validar_regras(regras):
        raise ValueError(
            "O arquivo regras.json possui uma estrutura inválida."
        )

    return regras