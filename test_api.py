from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_api_analisar():

    resposta = client.post(
        "/analisar",
        json={
            "texto": "O processo contém informações cadastrais do servidor."
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
                "O processo contém informações cadastrais "
                "e também o requerimento de aposentadoria."
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
            "texto": "O processo contém INFORMACOES CADASTRAIS do servidor."
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["resultado"] is True
    assert dados["quantidade_itens"] == 1
    assert dados["itens_encontrados"][0]["item"] == "Informações Cadastrais"

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
    Após análise dos dados funcionais do servidor, foram identificados
    quinquênios e dados financeiros atuais.

    Na matriz de apuração de tempo, foi considerado o
    Art. 147 do ADCT, EC 104_2020.
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
    assert dados["quantidade_itens"] == 2

    itens = dados["itens_encontrados"]

    nomes = [item["item"] for item in itens]

    assert "Dados Funcionais" in nomes
    assert "Matriz de Apuração de Tempo" in nomes

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
                "tipo": "Requerimento de Aposentadoria Regra de Transição",
                "numero": "111229178",
                "conteudo": "REQUERIMENTO DE APOSENTADORIA",
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

    assert resultado["resultado"] is True
    assert resultado["numero_processo"] == "1260.01.0068343/2025-37"
    assert resultado["quantidade_documentos"] == 1

    assert len(resultado["itens_encontrados"]) == 1

    assert resultado["itens_encontrados"][0]["id"] == "AP003"

    assert resultado["itens_encontrados"][0]["item"] == (
        "Requerimento de Aposentadoria"
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

    assert resultado["resultado"] is True

    assert resultado["numero_processo"] == (
        "1260.01.0068343/2025-37"
    )

    assert resultado["quantidade_documentos"] == 16

    assert isinstance(
        resultado["itens_encontrados"],
        list
    )

    ids_encontrados = [
        item["id"]
        for item in resultado["itens_encontrados"]
    ]

    assert "AP002" in ids_encontrados
    assert "AP003" in ids_encontrados
    assert "AP005" in ids_encontrados

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
        "Nenhum item previsto nas regras foi identificado no processo."
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

    assert resultado["resultado"] is True

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

    assert resultado["resultado"] is True
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