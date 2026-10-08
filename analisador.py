import re

from normalizador import normalizar_texto


def analisar_texto(texto: str, regras: list) -> list:

    texto_normalizado = normalizar_texto(texto)

    itens_encontrados = []

    for regra in regras:
        if not regra.get("ativo", True):
            continue

        padroes = regra["padroes"]

        criterio = regra.get("criterio", "qualquer")

        ocorrencias = [re.search(padrao, texto_normalizado) for padrao in padroes]

        if criterio == "todos":
            encontrado = all(ocorrencias)
        else:
            encontrado = any(ocorrencias)

        if encontrado:
            itens_encontrados.append({"id": regra.get("id"), "item": regra["item"]})

    return itens_encontrados
