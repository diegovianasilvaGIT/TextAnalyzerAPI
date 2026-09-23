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

def test_dados_funcionais_nao_identificado_pelo_nome_do_item():
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

    texto = "O documento apresenta a seção Dados Funcionais."

    resultado = analisar_texto(texto, regras)

    assert resultado == []


def test_dados_funcionais_identificado_por_ferias_premio():
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

    texto = "O servidor possui 3 períodos de FÉRIAS PRÊMIO."

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Dados Funcionais"


def test_dados_funcionais_identificado_por_quinquenios():
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

    texto = "O servidor possui direito a QUINQUÊNIOS."

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Dados Funcionais"


def test_dados_funcionais_identificado_por_dados_financeiros():
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

    texto = "Foram conferidos os DADOS FINANCEIROS ATUAIS."

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Dados Funcionais"

def test_item_aparece_uma_unica_vez_mesmo_com_multiplas_ocorrencias():
    regras = [
        {
            "item": "Requerimento de Aposentadoria",
            "fragmentos": [
                "requerimento de aposentadoria",
                "requerimento para aposentadoria"
            ]
        }
    ]

    texto = (
        "O requerimento de aposentadoria foi protocolado. "
        "Posteriormente, o requerimento de aposentadoria foi analisado. "
        "Ao final, o requerimento de aposentadoria foi deferido."
    )

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Requerimento de Aposentadoria"

def test_analise_ignora_maiusculas_e_minusculas():
    regras = [
        {
            "item": "Requerimento de Aposentadoria",
            "fragmentos": [
                "requerimento de aposentadoria"
            ]
        }
    ]

    texto = "REQUERIMENTO DE APOSENTADORIA"

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Requerimento de Aposentadoria"


def test_analise_ignora_acentos():
    regras = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": [
                "informações cadastrais"
            ]
        }
    ]

    texto = "informacoes cadastrais"

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Informações Cadastrais"


def test_analise_ignora_maiusculas_e_acentos_ao_mesmo_tempo():
    regras = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": [
                "informações cadastrais"
            ]
        }
    ]

    texto = "INFORMACOES CADASTRAIS"

    resultado = analisar_texto(texto, regras)

    assert len(resultado) == 1
    assert resultado[0]["item"] == "Informações Cadastrais"

def test_analisar_documento_com_varios_itens():

    regras = [
        {
            "item": "Certidão de Tempo Averbado",
            "fragmentos": [
                "Tempo Averbado",
                "Certidão de Tempo Averbado"
            ]
        },
        {
            "item": "Informações Cadastrais",
            "fragmentos": [
                "dados cadastrais",
                "informações cadastrais"
            ]
        },
        {
            "item": "Requerimento de Aposentadoria",
            "fragmentos": [
                "requerimento de aposentadoria",
                "requerimento para aposentadoria"
            ]
        },
        {
            "item": "Matriz de Apuração de Tempo",
            "fragmentos": [
                "Art. 144 do ADCT, EC 104_2020 cc Art. 40, III",
                "Art. 144 do ADCT, EC 104_2020 CC Art. 6",
                "Art. 146 do ADCT, EC 104 2020",
                "Art. 147 do ADCT, EC 104_2020",
                "Art. 149 do ADCT, EC 104"
            ]
        },
        {
            "item": "Dados Funcionais",
            "fragmentos": [
                "FÉRIAS PRÊMIO",
                "QUINQUÊNIOS",
                "DADOS FINANCEIROS ATUAIS"
            ]
        }
    ]

    texto = """
    Processo de aposentadoria do servidor.

    Foram analisadas as informações cadastrais do servidor,
    bem como o requerimento de aposentadoria apresentado.

    Também foi analisada a certidão de tempo averbado.

    Para a matriz de apuração de tempo, foi considerado o
    Art. 144 do ADCT, EC 104_2020 cc Art. 40, III.

    O documento também apresenta informações complementares
    sobre o histórico funcional do servidor.
    """

    resultado = analisar_texto(texto, regras)

    itens = [item["item"] for item in resultado]

    assert len(resultado) == 4

    assert "Certidão de Tempo Averbado" in itens
    assert "Informações Cadastrais" in itens
    assert "Requerimento de Aposentadoria" in itens
    assert "Matriz de Apuração de Tempo" in itens

    assert "Dados Funcionais" not in itens