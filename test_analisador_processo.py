from analisador_processo import analisar_documentos
from gerenciador_regras import carregar_regras, preparar_regras
from main import Documento

def test_analisar_documentos_encontra_declaracao_acumulo():

            documentos = [
                Documento(
                    data="01/01/2025",
                    tipo="Declaração de Acúmulo de Cargos/Proventos",
                    numero="111229178",
                    conteudo="""
                    DECLARAÇÃO DE ACÚMULO DE CARGOS
                    PROVENTOS
                    """,
                    assinaturas=[],
                    content_type="text/plain",
                    unidade_geradora="TESTE"
                )
            ]

            regras = carregar_regras()
            regras = preparar_regras(regras)

            resultado = analisar_documentos(documentos, regras)

            assert len(resultado) == 1

            assert resultado[0]["id"] == "AP003"

            assert resultado[0]["item"] == (
                "Declaração de Acúmulo de Cargos/Proventos"
            )

            assert resultado[0]["documentos"][0]["tipo"] == (
                "Declaração de Acúmulo de Cargos/Proventos"
            )

            assert resultado[0]["documentos"][0]["numero"] == "111229178"


def test_analisar_documentos_identifica_regras():


        documentos = [
            Documento(
                data="01/01/2025",
                tipo="Declaração de Acúmulo de Cargos/Proventos",
                numero="001",
                conteudo=(
                    "DECLARAÇÃO DE ACÚMULO DE CARGOS. "
                    "PROVENTOS."
                ),
                assinaturas=[],
                content_type="text/plain",
                unidade_geradora="TESTE"
            ),
            Documento(
                data="01/01/2025",
                tipo="Documento de identidade",
                numero="002",
                conteudo="CARTEIRA DE IDENTIDADE",
                assinaturas=[],
                content_type="text/plain",
                unidade_geradora="TESTE"
            ),
            Documento(
                data="01/01/2025",
                tipo="Tempo Averbado",
                numero="003",
                conteudo=(
                    "INFORMAÇÕES COMPLEMENTARES À APOSENTADORIA. "
                    "TEMPO AVERBADO. "
                    "TEMPO DE SERVIÇO."
                ),
                assinaturas=[],
                content_type="text/plain",
                unidade_geradora="TESTE"
            ),
            Documento(
                data="01/01/2025",
                tipo="Matriz de Contagem de Tempo",
                numero="004",
                conteudo=(
                    "Matriz de Contagem de Tempo. "
                    "Tempo de Serviço. "
                    "Contribuição."
                ),
                assinaturas=[],
                content_type="text/plain",
                unidade_geradora="TESTE"
            ),
            Documento(
                data="01/01/2025",
                tipo="Demonstrativo de pagamento",
                numero="005",
                conteudo="CONTRACHEQUE",
                assinaturas=[],
                content_type="text/plain",
                unidade_geradora="TESTE"
            )
        ]

        regras = carregar_regras()
        regras = preparar_regras(regras)

        resultado = analisar_documentos(documentos, regras)

        itens = [resultado_item["item"] for resultado_item in resultado]

        assert "Declaração de Acúmulo de Cargos/Proventos" in itens
        assert "Documento de identidade" in itens
        assert "Tempo Averbado" in itens
        assert "Matriz de Contagem de Tempo" in itens
        assert "Demonstrativo de pagamento do mês de vigência aposentadoria" in itens


def test_analisar_documentos_preserva_id_da_regra():


            documentos = [
                Documento(
                    data="01/01/2025",
                    tipo="Requerimento de Aposentadoria Regra de Transição",
                    numero="111229178",
                    conteudo="""
                    REQUERIMENTO DE APOSENTADORIA
                    REGRAS DE TRANSIÇÃO
                    """,
                    assinaturas=[],
                    content_type="text/plain",
                    unidade_geradora="TESTE"
                )
            ]

            regras = [
                {
                    "id": "AP003",
                    "item": "Requerimento de Aposentadoria",
                    "padroes": [
                        r"\brequerimento\ de\ aposentadoria\b"
                    ]
                }
            ]

            resultado = analisar_documentos(documentos, regras)

            assert resultado[0]["id"] == "AP003"


def test_analisar_documentos_identifica_fragmento():


            documentos = [
                Documento(
                    data="01/01/2025",
                    tipo="Requerimento de Aposentadoria",
                    numero="123456",
                    conteudo="REQUERIMENTO DE APOSENTADORIA",
                    assinaturas=[],
                    content_type="text/plain",
                    unidade_geradora="TESTE"
                )
            ]

            regras = [
                {
                    "id": "AP003",
                    "item": "Requerimento de Aposentadoria",
                    "fragmentos": [
                        "requerimento de aposentadoria",
                        "requerimento para aposentadoria"
                    ]
                }
            ]

            regras = preparar_regras(regras)

            resultado = analisar_documentos(
                documentos,
                regras
            )

            assert len(resultado) == 1

            assert resultado[0]["id"] == "AP003"

            assert resultado[0]["item"] == (
                "Requerimento de Aposentadoria"
            )

            assert resultado[0]["documentos"][0]["numero"] == "123456"

            assert resultado[0]["documentos"][0]["fragmentos"][0][
                "fragmento_regra"
            ] == "requerimento de aposentadoria"

def test_analisar_documentos_identifica_trecho_encontrado():


        documentos = [
            Documento(
                data="01/01/2025",
                tipo="Requerimento de Aposentadoria",
                numero="123456",
                conteudo=(
                    "O servidor apresentou REQUERIMENTO DE APOSENTADORIA "
                    "para análise."
                ),
                assinaturas=[],
                content_type="text/plain",
                unidade_geradora="TESTE"
            )
        ]

        regras = [
            {
                "id": "AP003",
                "item": "Requerimento de Aposentadoria",
                "fragmentos": [
                    "requerimento de aposentadoria"
                ]
            }
        ]

        regras = preparar_regras(regras)

        resultado = analisar_documentos(
            documentos,
            regras
        )

        documento_resultado = resultado[0]["documentos"][0]

        assert documento_resultado["fragmentos"][0][
            "fragmento_regra"
        ] == "requerimento de aposentadoria"

        assert documento_resultado["fragmentos"][0][
            "trecho_encontrado"
        ] == "requerimento de aposentadoria"


def test_regra_criterio_todos_nao_identifica_com_apenas_um_fragmento():


            documentos = [
                Documento(
                    data="01/01/2025",
                    tipo="FIPA",
                    numero="123456",
                    conteudo="O servidor possui FÉRIAS PRÊMIO.",
                    assinaturas=[],
                    content_type="text/plain",
                    unidade_geradora="TESTE"
                )
            ]

            regras = [
                {
                    "id": "AP005",
                    "item": "Dados Funcionais",
                    "criterio": "todos",
                    "fragmentos": [
                        "FÉRIAS PRÊMIO",
                        "QUINQUÊNIOS",
                        "DADOS FINANCEIROS ATUAIS"
                    ]
                }
            ]

            regras = preparar_regras(regras)

            resultado = analisar_documentos(
                documentos,
                regras
            )

            assert resultado == []


def test_regra_criterio_todos_nao_identifica_com_dois_fragmentos():


            documentos = [
                Documento(
                    data="01/01/2025",
                    tipo="FIPA",
                    numero="123456",
                    conteudo=(
                        "FÉRIAS PRÊMIO. "
                        "QUINQUÊNIOS."
                    ),
                    assinaturas=[],
                    content_type="text/plain",
                    unidade_geradora="TESTE"
                )
            ]

            regras = [
                {
                    "id": "AP005",
                    "item": "Dados Funcionais",
                    "criterio": "todos",
                    "fragmentos": [
                        "FÉRIAS PRÊMIO",
                        "QUINQUÊNIOS",
                        "DADOS FINANCEIROS ATUAIS"
                    ]
                }
            ]

            regras = preparar_regras(regras)

            resultado = analisar_documentos(
                documentos,
                regras
            )

            assert resultado == []


def test_regra_criterio_todos_identifica_com_todos_os_fragmentos():


            documentos = [
                Documento(
                    data="01/01/2025",
                    tipo="FIPA",
                    numero="123456",
                    conteudo=(
                        "FÉRIAS PRÊMIO. "
                        "QUINQUÊNIOS. "
                        "DADOS FINANCEIROS ATUAIS."
                    ),
                    assinaturas=[],
                    content_type="text/plain",
                    unidade_geradora="TESTE"
                )
            ]

            regras = [
                {
                    "id": "AP005",
                    "item": "Dados Funcionais",
                    "criterio": "todos",
                    "fragmentos": [
                        "FÉRIAS PRÊMIO",
                        "QUINQUÊNIOS",
                        "DADOS FINANCEIROS ATUAIS"
                    ]
                }
            ]

            regras = preparar_regras(regras)

            resultado = analisar_documentos(
                documentos,
                regras
            )

            assert len(resultado) == 1

            assert resultado[0]["id"] == "AP005"

            assert resultado[0]["item"] == "Dados Funcionais"

            assert len(resultado[0]["documentos"]) == 1

            assert resultado[0]["documentos"][0]["numero"] == "123456"


def test_regra_qualquer_usa_estrutura_padronizada_de_fragmentos():


        documentos = [
            Documento(
                data="01/01/2025",
                tipo="FIPA",
                numero="001",
                conteudo="Tempo Averbado",
                assinaturas=[],
                content_type="text/plain",
                unidade_geradora="TESTE"
            )
        ]

        regras = [
            {
                "id": "AP001",
                "item": "Certidão de Tempo Averbado",
                "fragmentos": [
                    "Tempo Averbado"
                ],
                "padroes": [
                    r"\btempo\ averbado\b"
                ],
                "criterio": "qualquer"
            }
        ]

        resultado = analisar_documentos(
            documentos,
            regras
        )

        assert resultado == [
            {
                "id": "AP001",
                "item": "Certidão de Tempo Averbado",
                "documentos": [
                    {
                        "tipo": "FIPA",
                        "numero": "001",
                        "fragmentos": [
                            {
                                "fragmento_regra": "Tempo Averbado",
                                "trecho_encontrado": "tempo averbado"
                            }
                        ]
                    }
                ]
            }
]
