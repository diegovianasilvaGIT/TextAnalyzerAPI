# TextAnalyzerAPI

API desenvolvida em Python com FastAPI para identificação de itens e fragmentos de texto a partir de um conjunto de regras configuráveis.

## Sobre o projeto

O **TextAnalyzerAPI** recebe um texto por meio de uma requisição HTTP e verifica se determinados itens estão presentes no conteúdo enviado.

As regras de identificação ficam armazenadas no arquivo `regras.json`, permitindo adicionar ou alterar itens e fragmentos sem precisar modificar a lógica principal da API.

O projeto também possui testes automatizados para validar tanto a lógica de análise quanto o funcionamento do endpoint da API.

## Tecnologias utilizadas

* Python 3.14+
* FastAPI
* Pydantic
* Uvicorn
* Pytest
* JSON
* Git
* GitHub

## Estrutura do projeto

```text
TextAnalyzerAPI/
│
├── .gitignore
├── analisador.py
├── main.py
├── regras.json
├── test_analisador.py
├── test_api.py
├── test_main.http
└── README.md
```

### `main.py`

É o ponto de entrada da aplicação FastAPI.

Responsável por:

* criar a aplicação;
* carregar as regras;
* validar a estrutura do arquivo `regras.json`;
* receber as requisições;
* validar o texto recebido;
* retornar os resultados da análise.

### `analisador.py`

Contém a lógica responsável pela análise dos textos.

Entre suas funções estão:

* normalização do texto;
* remoção de acentos para comparação;
* comparação sem diferenciação entre letras maiúsculas e minúsculas;
* identificação dos fragmentos;
* validação da estrutura das regras.

### `regras.json`

Arquivo que contém as regras utilizadas pela API.

Cada regra possui um `item` e uma lista de `fragmentos` que podem identificar esse item.

Exemplo:

```json
{
  "item": "Informações Cadastrais",
  "fragmentos": [
    "dados cadastrais",
    "informações cadastrais"
  ]
}
```

### `test_analisador.py`

Contém os testes da lógica de análise e validação das regras.

### `test_api.py`

Contém os testes do endpoint da API.

### `test_main.http`

Arquivo utilizado para realizar requisições HTTP diretamente pelo PyCharm.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/diegovianasilvaGIT/TextAnalyzerAPI.git
```

Entre na pasta do projeto:

```bash
cd TextAnalyzerAPI
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install fastapi uvicorn pytest httpx
```

## Executando a API

Com o ambiente virtual ativado, execute:

```powershell
python.exe -m uvicorn main:app --reload
```

A API ficará disponível localmente em:

```text
http://127.0.0.1:8000
```

## Documentação automática

O FastAPI disponibiliza uma interface interativa para testar a API.

Acesse:

```text
http://127.0.0.1:8000/docs
```

Também é possível acessar a documentação alternativa:

```text
http://127.0.0.1:8000/redoc
```

## Endpoint

### POST `/analisar`

Recebe um texto para análise.

Exemplo de requisição:

```json
{
  "texto": "Solicitação referente aos dados cadastrais do servidor."
}
```

Exemplo de resposta:

```json
{
  "resultado": true,
  "motivo": "Itens identificados no texto.",
  "quantidade_itens": 1,
  "itens_encontrados": [
    {
      "item": "Informações Cadastrais",
      "fragmento": "dados cadastrais"
    }
  ]
}
```

## Regras de identificação

A comparação realizada pela API não diferencia:

* letras maiúsculas e minúsculas;
* letras com ou sem acentos.

Por exemplo, as seguintes formas podem ser identificadas como equivalentes:

```text
FÉRIAS PRÊMIO
férias prêmio
ferias premio
FERIAS PREMIO
```

A comparação também considera palavras completas, evitando que um fragmento seja identificado apenas como parte de outra palavra.

## Resultado da análise

Quando um ou mais itens são identificados:

```json
{
  "resultado": true,
  "motivo": "Itens identificados no texto.",
  "quantidade_itens": 1,
  "itens_encontrados": []
}
```

Quando nenhum item é identificado:

```json
{
  "resultado": false,
  "motivo": "Nenhum item previsto nas regras foi identificado no texto.",
  "quantidade_itens": 0,
  "itens_encontrados": []
}
```

Quando o campo `texto` não é informado:

```json
{
  "resultado": false,
  "motivo": "O campo 'texto' é obrigatório.",
  "quantidade_itens": 0,
  "itens_encontrados": []
}
```

Quando o texto está vazio:

```json
{
  "resultado": false,
  "motivo": "O texto informado está vazio.",
  "quantidade_itens": 0,
  "itens_encontrados": []
}
```

## Testes

O projeto utiliza **Pytest** para testes automatizados.

Para executar todos os testes:

```powershell
python -m pytest
```

No estado atual do projeto, a suíte possui **18 testes automatizados**.

Resultado esperado:

```text
18 passed
```

## Adicionando novas regras

Para adicionar um novo item à análise, basta incluir uma nova regra no arquivo `regras.json`.

Exemplo:

```json
{
  "item": "Novo Item",
  "fragmentos": [
    "primeiro fragmento",
    "segundo fragmento"
  ]
}
```

A API utilizará automaticamente a nova regra na próxima execução.

## Objetivo do projeto

O projeto foi desenvolvido como uma aplicação prática para aprendizado de desenvolvimento de APIs em Python, utilizando FastAPI, testes automatizados, Git e GitHub.

A estrutura foi organizada para permitir a evolução futura da aplicação, incluindo novas regras, integrações e funcionalidades.
