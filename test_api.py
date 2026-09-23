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