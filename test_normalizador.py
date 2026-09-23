from normalizador import normalizar_texto


def test_normalizar_minusculas():

    resultado = normalizar_texto("DADOS CADASTRAIS")

    assert resultado == "dados cadastrais"


def test_normalizar_acentos():

    resultado = normalizar_texto("Informações Cadastrais")

    assert resultado == "informacoes cadastrais"


def test_normalizar_minusculas_e_acentos():

    resultado = normalizar_texto("REQUERIMENTO DE APOSENTADORIA")

    assert resultado == "requerimento de aposentadoria"