import re

from normalizador import normalizar_texto


def analisar_texto(texto: str, regras: list) -> list:

    texto_normalizado = normalizar_texto(texto)

    itens_encontrados = []

    for regra in regras:
        for padrao in regra["padroes"]:

            if re.search(padrao, texto_normalizado):
                itens_encontrados.append({
                    "item": regra["item"]
                })
                break

    return itens_encontrados