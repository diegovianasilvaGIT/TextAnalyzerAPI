import unicodedata
import re


def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    return texto


def analisar_texto(texto: str, regras: list) -> list:

    texto_normalizado = normalizar_texto(texto)

    itens_encontrados = []

    for regra in regras:
        for fragmento in regra["fragmentos"]:

            fragmento_normalizado = normalizar_texto(fragmento)
            padrao = r"\b" + re.escape(fragmento_normalizado) + r"\b"

            if re.search(padrao, texto_normalizado):
                itens_encontrados.append({
                    "item": regra["item"],
                    "fragmento": fragmento
                })
                break

    return itens_encontrados

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