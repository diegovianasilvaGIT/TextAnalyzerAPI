import json

from fastapi.testclient import TestClient
from main import app

from analisador import validar_regras, analisar_texto


client = TestClient(app)

def test_regras_validas():

    with open("regras.json", "r", encoding="utf-8") as arquivo:
        regras = json.load(arquivo)

    resultado = validar_regras(regras)

    assert resultado is True

def test_regra_sem_item():

    regras_invalidas = [
        {
            "fragmentos": [
                "informações cadastrais"
            ]
        }
    ]

    resultado = validar_regras(regras_invalidas)

    assert resultado is False

def test_regra_sem_fragmentos():

    regras_invalidas = [
        {
            "item": "Informações Cadastrais"
        }
    ]

    resultado = validar_regras(regras_invalidas)

    assert resultado is False

def test_fragmentos_vazios():

    regras_invalidas = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": []
        }
    ]

    resultado = validar_regras(regras_invalidas)

    assert resultado is False

def test_analisar_texto_com_item():

    regras = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": [
                "dados cadastrais",
                "informações cadastrais"
            ]
        }
    ]

    texto = "O processo contém informações cadastrais do servidor."

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Informações Cadastrais"

def test_analisar_texto_sem_item():

    regras = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": [
                "dados cadastrais",
                "informações cadastrais"
            ]
        }
    ]

    texto = "O processo contém documentos administrativos."

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 0

def test_analisar_texto_encontra_um_dos_fragmentos():
    regras = [
        {
            "item": "Requerimento de Aposentadoria",
            "fragmentos": [
                "requerimento de aposentadoria",
                "requerimento para aposentadoria"
            ]
        }
    ]

    texto = "Foi apresentado o requerimento para aposentadoria."

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Requerimento de Aposentadoria"
    assert resultado[0]["fragmento"] == "requerimento para aposentadoria"

def test_analisar_matriz_apuracao_tempo():
    regras = [
        {
            "item": "Matriz de Apuração de Tempo",
            "fragmentos": [
                "Art. 144 do ADCT, EC 104_2020 cc Art. 40, III",
                "Art. 144 do ADCT, EC 104_2020 CC Art. 6",
                "Art. 146 do ADCT, EC 104 2020",
                "Art. 147 do ADCT, EC 104_2020",
                "Art. 149 do ADCT, EC 104"
            ]
        }
    ]

    texto = (
        "Conforme o Art. 147 do ADCT, EC 104_2020, "
        "deve ser realizada a apuração."
    )

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Matriz de Apuração de Tempo"
    assert resultado[0]["fragmento"] == "Art. 147 do ADCT, EC 104_2020"

def test_analisar_dados_funcionais():
    regras = [
        {
            "item": "Dados Funcionais",
            "fragmentos": [
                "FÉRIAS PRÊMIO",
                "QUINQUÊNIOS",
                "DADOS FINANCEIROS ATUAIS"
            ]
        }
    ]

    texto = "O servidor possui informações sobre quinquênios."

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Dados Funcionais"
    assert resultado[0]["fragmento"] == "QUINQUÊNIOS"