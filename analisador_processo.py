import re

from normalizador import normalizar_texto


def analisar_documentos(documentos: list, regras: list) -> list:

    resultados = []

    for regra in regras:

        documentos_encontrados = []

        criterio = regra.get("criterio", "qualquer")

        for documento in documentos:

            conteudo_normalizado = normalizar_texto(
                documento.conteudo
            )

            correspondencias = []

            for indice, padrao in enumerate(regra["padroes"]):

                correspondencia = re.search(
                    padrao,
                    conteudo_normalizado
                )

                if correspondencia:
                    correspondencias.append(
                        {
                            "indice": indice,
                            "correspondencia": correspondencia
                        }
                    )

            if criterio == "todos":

                if len(correspondencias) != len(regra["padroes"]):
                    continue

                indices_encontrados = {
                    item["indice"]
                    for item in correspondencias
                }

                if len(indices_encontrados) != len(regra["padroes"]):
                    continue

                documento_resultado = {
                    "tipo": documento.tipo,
                    "numero": documento.numero
                }

                documento_resultado["fragmentos"] = [
                    {
                        "fragmento_regra": regra["fragmentos"][item["indice"]],
                        "trecho_encontrado": (
                            item["correspondencia"].group(0)
                        )
                    }
                    for item in correspondencias
                ]

                documentos_encontrados.append(
                    documento_resultado
                )

            else:

                if not correspondencias:
                    continue

                item_encontrado = correspondencias[0]

                indice = item_encontrado["indice"]

                fragmento_regra = None
                trecho_encontrado = None

                if "fragmentos" in regra:
                    fragmento_regra = regra["fragmentos"][indice]

                    trecho_encontrado = (
                        item_encontrado["correspondencia"].group(0)
                    )

                documento_resultado = {
                    "tipo": documento.tipo,
                    "numero": documento.numero,
                    "fragmentos": []
                }

                if fragmento_regra is not None:
                    documento_resultado["fragmentos"].append(
                        {
                            "fragmento_regra": fragmento_regra,
                            "trecho_encontrado": trecho_encontrado
                        }
                    )

                documentos_encontrados.append(
                    documento_resultado
                )

        if documentos_encontrados:
            resultados.append({
                "id": regra.get("id"),
                "item": regra["item"],
                "documentos": documentos_encontrados
            })

    return resultados