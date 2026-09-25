from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_api_analisar():

    resposta = client.post(
        "/analisar",
        json={
            "texto": "O processo contém um contracheque do servidor."
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is True
    assert dados["quantidade_itens"] == 1

def test_api_texto_vazio():

    resposta = client.post(
        "/analisar",
        json={
            "texto": ""
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is False
    assert dados["quantidade_itens"] == 0
    assert dados["motivo"] == "O texto informado está vazio."

def test_api_sem_item():
    resposta = client.post(
        "/analisar",
        json={
            "texto": "O processo contém documentos administrativos."
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is False
    assert dados["quantidade_itens"] == 0
    assert dados["itens_encontrados"] == []
    assert dados["motivo"] == "Nenhum item previsto nas regras foi identificado no texto."

def test_api_com_varios_itens():
    resposta = client.post(
        "/analisar",
        json={
            "texto": (
                "O processo contém uma carteira de identidade "
                "e também um contracheque do servidor."
            )
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is True
    assert dados["quantidade_itens"] == 2
    assert len(dados["itens_encontrados"]) == 2

def test_api_sem_acento_e_maiusculas():
    resposta = client.post(
        "/analisar",
        json={
            "texto": "O processo contém CERTIDAO DE NASCIMENTO do servidor."
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is True
    assert dados["quantidade_itens"] == 1
    assert dados["itens_encontrados"][0]["item"] == (
        "Documento de identidade"
    )

def test_api_sem_campo_texto_retorna_motivo():
    resposta = client.post(
        "/analisar",
        json={}
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is False
    assert dados["motivo"] == "O campo 'texto' é obrigatório."

def test_api_texto_tipo_invalido():
    resposta = client.post(
        "/analisar",
        json={
            "texto": 12345
        }
    )

    assert resposta.status_code == 422

def test_api_texto_nulo():
    resposta = client.post(
        "/analisar",
        json={
            "texto": None
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is False
    assert dados["motivo"] == "O campo 'texto' é obrigatório."
    assert dados["quantidade_itens"] == 0
    assert dados["itens_encontrados"] == []

def test_api_texto_realista():
    texto = """
    Após análise do processo, foi emitido o RELATÓRIO PARA CONFERÊNCIA.

    Foram verificadas as informações de FÉRIAS PRÊMIO,
    QUINQUÊNIOS, BIÊNIOS e DADOS FINANCEIROS do servidor.
    """

    resposta = client.post(
        "/analisar",
        json={
            "texto": texto
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is True
    assert dados["quantidade_itens"] == 1

    itens = dados["itens_encontrados"]

    assert itens[0]["id"] == "AP002"
    assert itens[0]["item"] == "Conferencia Dados Funcionais"

def test_api_rejeita_texto_nulo():
    resposta = client.post(
        "/analisar",
        json={"texto": None}
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is False
    assert dados["motivo"] == "O campo 'texto' é obrigatório."
    assert dados["quantidade_itens"] == 0
    assert dados["itens_encontrados"] == []


def test_api_rejeita_texto_vazio():
    resposta = client.post(
        "/analisar",
        json={"texto": ""}
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is False
    assert dados["motivo"] == "O texto informado está vazio."
    assert dados["quantidade_itens"] == 0
    assert dados["itens_encontrados"] == []


def test_api_rejeita_texto_apenas_com_espacos():
    resposta = client.post(
        "/analisar",
        json={"texto": "     "}
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is False
    assert dados["motivo"] == "O texto informado está vazio."
    assert dados["quantidade_itens"] == 0
    assert dados["itens_encontrados"] == []

def test_api_rejeita_campo_texto_ausente():
    resposta = client.post(
        "/analisar",
        json={}
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is False
    assert dados["motivo"] == "O campo 'texto' é obrigatório."
    assert dados["quantidade_itens"] == 0
    assert dados["itens_encontrados"] == []

def test_api_rejeita_texto_numerico():

    resposta = client.post(
        "/analisar",
        json={"texto": 123}
    )

    assert resposta.status_code == 422

    dados = resposta.json()

    assert dados["detail"][0]["type"] == "string_type"
    assert dados["detail"][0]["loc"] == ["body", "texto"]

def test_validar_processo_realiza_analise():

    payload = {
        "processo": {
            "numero": "1260.01.0068343/2025-37"
        },
        "documentos": [
            {
                "data": "01/01/2025",
                "tipo": "Demonstrativo de pagamento",
                "numero": "111229178",
                "conteudo": "CONTRACHEQUE DO SERVIDOR",
                "assinaturas": [],
                "content_type": "text/plain",
                "unidade_geradora": "TESTE"
            }
        ]
    }

    response = client.post(
        "/validar-processo",
        json=payload
    )

    assert response.status_code == 200

    resultado = response.json()

    assert resultado["resultado"] is False
    assert "itens_nao_encontrados" in resultado
    assert resultado["numero_processo"] == "1260.01.0068343/2025-37"
    assert resultado["quantidade_documentos"] == 1

    assert len(resultado["itens_encontrados"]) == 1

    assert resultado["itens_encontrados"][0]["id"] == "AP009"

    assert resultado["itens_encontrados"][0]["item"] == (
        "Demonstrativo de pagamento do mês de vigência aposentadoria"
    )

    assert resultado["itens_encontrados"][0]["documentos"][0]["numero"] == (
        "111229178"
    )
def test_validar_processo_real_com_json_completo():

    import json
    from pathlib import Path

    caminho = Path(__file__).resolve().parent / "processo 1.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        payload = json.load(arquivo)

    response = client.post(
        "/validar-processo",
        json=payload
    )

    assert response.status_code == 200

    resultado = response.json()

    assert resultado["resultado"] is False

    assert resultado["numero_processo"] == (
        "1260.01.0068343/2025-37"
    )

    assert resultado["quantidade_documentos"] == 16

    assert isinstance(
        resultado["itens_encontrados"],
        list
    )
    ids_nao_encontrados = [
        item["id"]
        for item in resultado["itens_nao_encontrados"]
    ]

    assert ids_nao_encontrados == [
        "AP005",
        "AP006",
        "AP007",
        "AP008"
    ]

    assert "itens_nao_encontrados" in resultado
    assert isinstance(
        resultado["itens_nao_encontrados"],
        list
    )

    ids_encontrados = [
        item["id"]
        for item in resultado["itens_encontrados"]
    ]

    assert "AP002" in ids_encontrados
    assert "AP003" in ids_encontrados

    ap002 = next(
        item
        for item in resultado["itens_encontrados"]
        if item["id"] == "AP002"
    )

    assert "documentos" in ap002
    assert isinstance(ap002["documentos"], list)
    assert len(ap002["documentos"]) > 0

    documento_ap002 = ap002["documentos"][0]

    assert "tipo" in documento_ap002
    assert "numero" in documento_ap002
    assert "fragmentos" in documento_ap002
    assert isinstance(
        documento_ap002["fragmentos"],
        list
    )

    assert len(documento_ap002["fragmentos"]) == 5

    fragmentos_ap002 = [
        fragmento["fragmento_regra"]
        for fragmento in documento_ap002["fragmentos"]
    ]

    for fragmento in [
        "RELATÓRIO PARA CONFERÊNCIA",
        "FÉRIAS PRÊMIO",
        "QUINQUÊNIOS",
        "BIÊNIOS",
        "DADOS FINANCEIROS"
    ]:
        assert fragmento in fragmentos_ap002

    for fragmento in documento_ap002["fragmentos"]:
        assert "fragmento_regra" in fragmento
        assert "trecho_encontrado" in fragmento
        assert fragmento["trecho_encontrado"]

    ap009 = next(
        item
        for item in resultado["itens_encontrados"]
        if item["id"] == "AP009"
    )

    assert "documentos" in ap009
    assert isinstance(ap009["documentos"], list)
    assert len(ap009["documentos"]) > 0

    documento_ap009 = ap009["documentos"][0]

    assert "tipo" in documento_ap009
    assert "numero" in documento_ap009
    assert "fragmentos" in documento_ap009
    assert isinstance(
        documento_ap009["fragmentos"],
        list
    )

    assert len(documento_ap009["fragmentos"]) >= 1

    for fragmento in documento_ap009["fragmentos"]:
        assert "fragmento_regra" in fragmento
        assert "trecho_encontrado" in fragmento
        assert fragmento["trecho_encontrado"]

def test_validar_processo_sem_itens_encontrados():

    payload = {
        "processo": {
            "numero": "9999.99.9999999/9999-99"
        },
        "documentos": [
            {
                "data": "01/01/2025",
                "tipo": "Documento de Teste",
                "numero": "999999",
                "conteudo": "Este documento não possui nenhum fragmento previsto.",
                "assinaturas": [],
                "content_type": "text/plain",
                "unidade_geradora": "TESTE"
            }
        ]
    }

    response = client.post(
        "/validar-processo",
        json=payload
    )

    assert response.status_code == 200

    resultado = response.json()

    assert resultado["resultado"] is False

    assert resultado["motivo"] == (
        "Existem itens obrigatórios não encontrados no processo."
    )

    assert resultado["quantidade_documentos"] == 1

    assert resultado["itens_encontrados"] == []

def test_validar_processo_real_com_processo_json():

    import json
    from pathlib import Path

    caminho = Path(__file__).resolve().parent / "processo.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        payload = json.load(arquivo)

    response = client.post(
        "/validar-processo",
        json=payload
    )

    assert response.status_code == 200

    resultado = response.json()

    assert resultado["resultado"] is False

    assert resultado["numero_processo"] == (
        "1450.01.0035106/2023-81"
    )

    assert resultado["quantidade_documentos"] == 17

    assert isinstance(
        resultado["itens_encontrados"],
        list
    )

    assert len(resultado["itens_encontrados"]) > 0

def test_api_validar_processo_com_json_real():
    import json
    from pathlib import Path

    caminho = Path(__file__).resolve().parent / "processo.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    resposta = client.post(
        "/validar-processo",
        json=dados
    )

    assert resposta.status_code == 200

    resultado = resposta.json()

    assert resultado["resultado"] is False
    assert resultado["numero_processo"] == "1450.01.0035106/2023-81"
    assert resultado["quantidade_documentos"] == 17

    ids_encontrados = [
        item["id"]
        for item in resultado["itens_encontrados"]
    ]

    assert "AP001" in ids_encontrados
    assert "AP002" in ids_encontrados
    assert "AP003" in ids_encontrados
    assert "AP005" in ids_encontrados
    print("\nResposta completa da API:")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))

