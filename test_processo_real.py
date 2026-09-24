import json
from pathlib import Path

from analisador_processo import analisar_documentos
from gerenciador_regras import carregar_regras, preparar_regras
from main import ProcessoRequest


def test_analisar_processo_real():

    caminho = Path(__file__).resolve().parent / "processo 1.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados_json = json.load(arquivo)

    processo = ProcessoRequest(**dados_json)

    regras = carregar_regras()
    regras = preparar_regras(regras)

    resultado = analisar_documentos(
        processo.documentos,
        regras
    )

    assert len(processo.documentos) == 16

    assert isinstance(resultado, list)

    ids_encontrados = [
        item["id"]
        for item in resultado
    ]

    assert "AP002" in ids_encontrados
    assert "AP003" in ids_encontrados
    assert "AP005" in ids_encontrados

    ap005 = next(
        item
        for item in resultado
        if item["id"] == "AP005"
    )

    assert len(ap005["documentos"]) == 1

    documento_ap005 = ap005["documentos"][0]

    assert documento_ap005["numero"] == "111228515"

    assert documento_ap005["fragmentos"] == [
        {
            "fragmento_regra": "FÉRIAS PRÊMIO",
            "trecho_encontrado": "ferias premio"
        },
        {
            "fragmento_regra": "QUINQUÊNIOS",
            "trecho_encontrado": "quinquenios"
        },
        {
            "fragmento_regra": "DADOS FINANCEIROS ATUAIS",
            "trecho_encontrado": "dados financeiros atuais"
        }
    ]

    print("\nResultado da análise:")

    for item in resultado:

        print(
            f"\n{item['id']} - {item['item']}"
        )

        for documento in item["documentos"]:

            print(
                f"  - {documento['tipo']} "
                f"| {documento['numero']}"
            )

def test_analisar_primeiro_processo_real():

    caminho = Path(__file__).resolve().parent / "processo.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados_json = json.load(arquivo)

    processo = ProcessoRequest(**dados_json)

    regras = carregar_regras()
    regras = preparar_regras(regras)

    resultado = analisar_documentos(
        processo.documentos,
        regras
    )

    assert len(processo.documentos) == 17
    assert isinstance(resultado, list)

    print("\n\nResultado do processo:")
    print(processo.processo.numero)

    for item in resultado:

        print(
            f"\n{item['id']} - {item['item']}"
        )

        for documento_resultado in item["documentos"]:

            print(
                f"  - {documento_resultado['tipo']} "
                f"| {documento_resultado['numero']}"
            )

            if "fragmento_regra" in documento_resultado:
                print(
                    f"    Regra: "
                    f"{documento_resultado['fragmento_regra']}"
                )

            if "trecho_encontrado" in documento_resultado:
                print(
                    f"    Encontrado: "
                    f"{documento_resultado['trecho_encontrado']}"
                )

            for documento_original in processo.documentos:

                if (
                    documento_original.numero
                    == documento_resultado["numero"]
                ):
                    print("    CONTEÚDO:")
                    print(
                        documento_original.conteudo[:500]
                    )
                    print("    ...")
                    break