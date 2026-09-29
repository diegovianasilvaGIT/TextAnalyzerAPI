# TextAnalyzerAPI

API desenvolvida em Python com FastAPI para análise e validação de processos a partir de um conjunto de regras configuráveis.

A aplicação identifica documentos e conteúdos relacionados aos itens obrigatórios definidos em `regras.json` e informa se um processo está completo ou quais itens ainda não foram identificados.

---

## 1. Objetivo

O **TextAnalyzerAPI** foi desenvolvido para receber informações de processos e seus documentos por meio de requisições HTTP.

A API analisa o conteúdo dos documentos utilizando regras configuráveis e retorna uma resposta simplificada para o sistema consumidor.

O principal cenário de integração é a validação de um processo:

* `resultado: true` → todos os itens ativos foram identificados;
* `resultado: false` → um ou mais itens não foram identificados;
* `itens_nao_encontrados` → lista dos itens que não foram identificados.

A lógica de identificação fica separada do contrato de integração, permitindo que o sistema consumidor receba apenas as informações necessárias para tomar sua decisão.

---

## 2. Tecnologias utilizadas

* Python 3.14+
* FastAPI
* Pydantic
* Uvicorn
* Pytest
* JSON
* Git
* GitHub

---

## 3. Estrutura do projeto

```text
TextAnalyzerAPI/
│
├── .gitignore
├── analisador.py
├── analisador_processo.py
├── gerenciador_regras.py
├── normalizador.py
├── main.py
├── regras.json
├── test_analisador.py
├── test_api.py
├── test_main.http
└── README.md
```

### `main.py`

Ponto de entrada da aplicação FastAPI.

Responsável por:

* criar a aplicação;
* definir os modelos de entrada;
* carregar as regras;
* disponibilizar os endpoints;
* receber e validar as requisições;
* retornar as respostas da API.

### `analisador.py`

Contém a lógica de análise de textos.

Entre suas responsabilidades estão:

* análise de fragmentos;
* identificação de itens;
* tratamento das regras;
* comparação dos textos conforme as regras configuradas.

### `analisador_processo.py`

Responsável pela análise dos documentos de um processo.

Para cada regra ativa, verifica os conteúdos dos documentos e identifica os fragmentos correspondentes.

Também registra:

* item identificado;
* documento em que foi identificado;
* fragmento da regra;
* trecho encontrado no documento.

### `gerenciador_regras.py`

Responsável por:

* carregar o arquivo `regras.json`;
* validar sua estrutura;
* preparar as regras para utilização;
* transformar os fragmentos em padrões de busca.

### `normalizador.py`

Responsável pela normalização dos textos utilizados durante as comparações.

### `regras.json`

Arquivo que contém as regras utilizadas pela API.

As regras podem ser alteradas ou adicionadas sem modificar a lógica principal da aplicação.

### `test_analisador.py`

Contém os testes da lógica de análise e das regras.

### `test_api.py`

Contém os testes dos endpoints da API.

### `test_main.http`

Arquivo utilizado para realizar requisições HTTP diretamente pelo PyCharm.

---

## 4. Instalação

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

```powershell
pip install fastapi uvicorn pytest httpx
```

---

## 5. Executando a API

Com o ambiente virtual ativado:

```powershell
python.exe -m uvicorn main:app --reload
```

A API ficará disponível localmente em:

```text
http://127.0.0.1:8000
```

---

## 6. Documentação automática

O FastAPI disponibiliza uma documentação interativa.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

A documentação apresenta automaticamente os modelos de entrada e os endpoints disponíveis.

---

# 7. Endpoints

## 7.1 POST `/analisar`

Endpoint utilizado para analisar um texto individualmente.

### Requisição

```json
{
  "texto": "Solicitação referente aos dados cadastrais do servidor."
}
```

### Resposta quando um item é identificado

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

### Resposta quando nenhum item é identificado

```json
{
  "resultado": false,
  "motivo": "Nenhum item previsto nas regras foi identificado no texto.",
  "quantidade_itens": 0,
  "itens_encontrados": []
}
```

### Texto vazio

```json
{
  "resultado": false,
  "motivo": "O texto informado está vazio.",
  "quantidade_itens": 0,
  "itens_encontrados": []
}
```

### Campo `texto` não informado

```json
{
  "resultado": false,
  "motivo": "O campo 'texto' é obrigatório.",
  "quantidade_itens": 0,
  "itens_encontrados": []
}
```

---

# 8. POST `/validar-processo`

Este é o principal endpoint destinado à integração com o sistema consumidor.

Recebe um processo e seus documentos e verifica se os itens previstos nas regras foram identificados.

---

## 8.1 Estrutura da requisição

```json
{
  "processo": {
    "numero": "1500.01.0000000/2026-00"
  },
  "documentos": [
    {
      "data": "2026-09-29",
      "tipo": "Documento",
      "numero": "001",
      "conteudo": "Conteúdo completo do documento.",
      "assinaturas": [
        {
          "cpf": "00000000000",
          "nome": "Nome do assinante"
        }
      ],
      "content_type": "application/pdf",
      "unidade_geradora": "SEPLAG"
    }
  ]
}
```

### Campos do processo

| Campo             | Tipo   | Descrição                        |
| ----------------- | ------ | -------------------------------- |
| `processo.numero` | string | Número identificador do processo |

### Campos dos documentos

| Campo              | Tipo   | Descrição                                     |
| ------------------ | ------ | --------------------------------------------- |
| `data`             | string | Data do documento                             |
| `tipo`             | string | Tipo do documento                             |
| `numero`           | string | Número ou identificador do documento          |
| `conteudo`         | string | Conteúdo textual analisado pela API           |
| `assinaturas`      | lista  | Assinaturas associadas ao documento           |
| `content_type`     | string | Tipo de conteúdo do documento                 |
| `unidade_geradora` | string | Unidade responsável pela geração do documento |

### Campos das assinaturas

| Campo  | Tipo   | Descrição         |
| ------ | ------ | ----------------- |
| `cpf`  | string | CPF do assinante  |
| `nome` | string | Nome do assinante |

---

# 9. Resposta do `/validar-processo`

A resposta foi projetada para ser simples para o sistema consumidor.

## 9.1 Processo completo

Quando todos os itens ativos das regras são identificados:

```json
{
  "resultado": true,
  "itens_nao_encontrados": []
}
```

### Interpretação

O sistema consumidor pode interpretar:

```text
resultado = true
```

como:

> O processo contém todos os itens previstos pelas regras ativas.

---

## 9.2 Processo incompleto

Quando um ou mais itens não são identificados:

```json
{
  "resultado": false,
  "itens_nao_encontrados": [
    "Documento de identidade",
    "Matriz de apuração de tempo de acordo à regra de aposentadoria"
  ]
}
```

### Interpretação

O sistema consumidor pode interpretar:

```text
resultado = false
```

como:

> Existem itens previstos pelas regras que não foram identificados no processo.

A lista `itens_nao_encontrados` informa quais itens não foram identificados.

---

# 10. Contrato para integração com o sistema Go

O sistema Go não precisa conhecer a implementação interna da API.

A integração pode considerar somente a seguinte resposta:

### Processo completo

```json
{
  "resultado": true,
  "itens_nao_encontrados": []
}
```

### Processo incompleto

```json
{
  "resultado": false,
  "itens_nao_encontrados": [
    "Item A",
    "Item B"
  ]
}
```

Portanto, a lógica de decisão do sistema consumidor pode ser baseada diretamente no campo:

```text
resultado
```

e, quando o resultado for `false`, consultar:

```text
itens_nao_encontrados
```

---

# 11. Regras de identificação

As regras utilizadas pela API ficam armazenadas em:

```text
regras.json
```

Cada regra possui, entre outras informações:

* identificador;
* item;
* situação ativa/inativa;
* critério;
* fragmentos.

Os identificadores das regras seguem a convenção:

```text
AP001
AP002
AP003
...
```

O prefixo `AP` é utilizado independentemente do item ou categoria da regra.

---

## 11.1 Critérios

As regras podem utilizar critérios diferentes para determinar a identificação de um item.

### Critério `qualquer`

O item pode ser identificado quando qualquer um dos fragmentos configurados for encontrado.

### Critério `todos`

O item somente é identificado quando todos os fragmentos necessários forem encontrados no mesmo documento, conforme a regra configurada.

---

# 12. Normalização

A API realiza a normalização dos textos antes das comparações.

A finalidade é permitir que diferenças de apresentação d
