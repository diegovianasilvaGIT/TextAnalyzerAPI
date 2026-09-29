from gerenciador_regras import (
    carregar_regras,
    validar_regras,
    preparar_regras
)


def test_carregar_regras_retorna_lista():

    regras = carregar_regras()

    assert isinstance(regras, list)


def test_carregar_regras_possui_regras():

    regras = carregar_regras()

    assert len(regras) > 0


def test_carregar_regras_possui_estrutura_valida():

    regras = carregar_regras()

    for regra in regras:
        assert "item" in regra
        assert "fragmentos" in regra
        assert isinstance(regra["fragmentos"], list)
        assert len(regra["fragmentos"]) > 0

def test_validar_regras_rejeita_valor_que_nao_e_lista():

    regras = {}

    assert validar_regras(regras) is False


def test_validar_regras_rejeita_regra_sem_item():

    regras = [
        {
            "fragmentos": ["dados cadastrais"]
        }
    ]

    assert validar_regras(regras) is False


def test_validar_regras_rejeita_regra_sem_fragmentos():

    regras = [
        {
            "item": "Informações Cadastrais"
        }
    ]

    assert validar_regras(regras) is False

def test_validar_regras_rejeita_fragmentos_que_nao_sao_lista():

    regras = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": "dados cadastrais"
        }
    ]

    assert validar_regras(regras) is False


def test_validar_regras_rejeita_fragmentos_vazios():

    regras = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": []
        }
    ]

    assert validar_regras(regras) is False


def test_validar_regras_rejeita_regra_que_nao_e_dicionario():

    regras = [
        "Informações Cadastrais"
    ]

    assert validar_regras(regras) is False

def test_preparar_regras_retorna_lista():

    regras = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": [
                "dados cadastrais"
            ]
        }
    ]

    resultado = preparar_regras(regras)

    assert isinstance(resultado, list)


def test_preparar_regras_preserva_item():

    regras = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": [
                "dados cadastrais"
            ]
        }
    ]

    resultado = preparar_regras(regras)

    assert resultado[0]["item"] == "Informações Cadastrais"


def test_preparar_regras_cria_padroes():

    regras = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": [
                "Dados Cadastrais"
            ]
        }
    ]

    resultado = preparar_regras(regras)

    assert "padroes" in resultado[0]
    assert len(resultado[0]["padroes"]) == 1

def test_preparar_regras_preserva_id():

    regras = [
        {
            "id": "AP003",
            "item": "Requerimento de Aposentadoria",
            "fragmentos": [
                "requerimento de aposentadoria"
            ]
        }
    ]

    resultado = preparar_regras(regras)

    assert resultado[0]["id"] == "AP003"

def test_preparar_regras_preserva_criterio():

    regras = [
        {
            "id": "AP005",
            "item": "Tempo Averbado",
            "ativo": True,
            "criterio": "todos",
            "fragmentos": [
                "INFORMAÇÕES COMPLEMENTARES À APOSENTADORIA",
                "TEMPO AVERBADO",
                "TEMPO DE SERVIÇO"
            ]
        }
    ]

    resultado = preparar_regras(regras)

    assert resultado[0]["criterio"] == "todos"

def test_preparar_regras_preserva_ativo():

    regras = [
        {
            "id": "AP001",
            "item": "Informações Cadastrais",
            "ativo": False,
            "criterio": "qualquer",
            "fragmentos": [
                "dados cadastrais"
            ]
        }
    ]

    resultado = preparar_regras(regras)

    assert resultado[0]["ativo"] is False

def test_validar_regras_rejeita_regra_sem_id():

    regras = [
        {
            "item": "Informações Cadastrais",
            "fragmentos": [
                "dados cadastrais"
            ]
        }
    ]

    assert validar_regras(regras) is False

def test_validar_regras_rejeita_id_que_nao_e_string():

    regras = [
        {
            "id": 123,
            "item": "Informações Cadastrais",
            "fragmentos": [
                "dados cadastrais"
            ]
        }
    ]

    assert validar_regras(regras) is False

def test_validar_regras_rejeita_ativo_que_nao_e_booleano():

    regras = [
        {
            "id": "AP001",
            "item": "Informações Cadastrais",
            "ativo": "sim",
            "fragmentos": [
                "dados cadastrais"
            ]
        }
    ]

    assert validar_regras(regras) is False

def test_validar_regras_rejeita_criterio_invalido():

    regras = [
        {
            "id": "AP001",
            "item": "Informações Cadastrais",
            "criterio": "qualquer-coisa",
            "fragmentos": [
                "dados cadastrais"
            ]
        }
    ]

    assert validar_regras(regras) is False

def test_validar_regras_rejeita_item_que_nao_e_string():

    regras = [
        {
            "id": "AP999",
            "item": 123,
            "ativo": True,
            "criterio": "qualquer",
            "fragmentos": [
                "TESTE"
            ]
        }
    ]

    assert validar_regras(regras) is False

def test_validar_regras_rejeita_fragmento_que_nao_e_string():

    regras = [
        {
            "id": "AP999",
            "item": "Regra de teste",
            "ativo": True,
            "criterio": "qualquer",
            "fragmentos": [
                "TESTE",
                123
            ]
        }
    ]

    assert validar_regras(regras) is False

def test_validar_regras_rejeita_fragmento_vazio():

    regras = [
        {
            "id": "AP999",
            "item": "Regra de teste",
            "ativo": True,
            "criterio": "qualquer",
            "fragmentos": [
                ""
            ]
        }
    ]

    assert validar_regras(regras) is False

def test_validar_regras_rejeita_id_vazio():

    regras = [
        {
            "id": "",
            "item": "Regra de teste",
            "ativo": True,
            "criterio": "qualquer",
            "fragmentos": [
                "TESTE"
            ]
        }
    ]

    assert validar_regras(regras) is False

def test_validar_regras_rejeita_item_vazio():

    regras = [
        {
            "id": "AP999",
            "item": "",
            "ativo": True,
            "criterio": "qualquer",
            "fragmentos": [
                "TESTE"
            ]
        }
    ]

    assert validar_regras(regras) is False