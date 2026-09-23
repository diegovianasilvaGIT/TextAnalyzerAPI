from fastapi import FastAPI
from pydantic import BaseModel, Field
import json

from analisador import analisar_texto, validar_regras

app = FastAPI(
    title="Text Analyzer API",
    description="API para identificação de itens e fragmentos em textos.",
    version="1.0.0"
)


class TextoEntrada(BaseModel):
    texto: str | None = Field(
        default=None,
        description="Texto que será analisado pela API."
    )

with open("regras.json", "r", encoding="utf-8") as arquivo:
    regras = json.load(arquivo)

    if not validar_regras(regras):
        raise ValueError("O arquivo regras.json possui uma estrutura inválida.")


@app.post("/analisar")
async def endpoint_analisar_texto(dados: TextoEntrada):

    if dados.texto is None:
        return {
            "resultado": False,
            "motivo": "O campo 'texto' é obrigatório.",
            "quantidade_itens": 0,
            "itens_encontrados": []
        }

    if not dados.texto.strip():
        return {
            "resultado": False,
            "motivo": "O texto informado está vazio.",
            "quantidade_itens": 0,
            "itens_encontrados": []
        }

    itens_encontrados = analisar_texto(dados.texto, regras)

    if len(itens_encontrados) > 0:
        return {
            "resultado": True,
            "motivo": "Itens identificados no texto.",
            "quantidade_itens": len(itens_encontrados),
            "itens_encontrados": itens_encontrados
        }

    return {
        "resultado": False,
        "motivo": "Nenhum item previsto nas regras foi identificado no texto.",
        "quantidade_itens": 0,
        "itens_encontrados": []
    }