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