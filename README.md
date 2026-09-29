# TextAnalyzerAPI

API desenvolvida em Python com FastAPI para análise e validação de processos a partir de um conjunto de regras configuráveis.

A aplicação identifica documentos e conteúdos relacionados aos itens obrigatórios definidos em `regras.json` e informa se um processo está completo ou quais itens ainda não foram identificados.

O principal cenário de utilização é a validação de processos relacionados à aposentadoria, permitindo que um sistema consumidor identifique processos que necessitam de diligência ou complementação documental.

---

## 1. Objetivo

O **TextAnalyzerAPI** recebe informações de processos e seus documentos por meio de requisições HTTP.

A API analisa o conteúdo textual dos documentos utilizando regras configuráveis e retorna uma resposta simplificada para o sistema consumidor.

O principal endpoint de integração é:

```text
POST /validar-processo
```

A resposta possui dois campos:

```json
{
  "resultado": true,
  "itens_nao_encontrados": []
}
```

### Interpretação

* `resultado: true` → todos os itens ativos configurados nas regras foram identificados;
* `resultado: false` → um ou mais itens ativos não foram identificados;
* `itens_nao_encontrados` → lista dos itens que não foram identificados.

A lógica interna de identificação fica separada do contrato de integração, permitindo que o sistema consumidor receba somente as informações necessárias para tomar sua decisão.

---

# 2. Tecnologias utilizadas

* Python 3.14+
* FastAPI
* Pydantic
* Uvicorn
* Pytest
* JSON
* Docker
* Git
* GitHub

As versões das principais dependências utilizadas pela aplicação estão fixadas no arquivo:

```text
requirements.txt
```

---

# 3. Estrutura do projeto

```text
TextAnalyzerAPI/
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── regras.json
│
├── main.py
├── analisador.py
├── analisador_processo.py
├── gerenciador_regras.py
└── normalizador.py
│
├── processo.json
├── processo 1.json
│
├── test_analisador.py
├── test_analisador_processo.py
├── test_api.py
├── test_gerenciador_regras.py
├── test_main.http
├── test_normalizador.py
└── test_processo_real.py
```

---

# 4. Componentes principais

## `main.py`

Ponto de entrada da aplicação FastAPI.

Responsável por:

* criar a aplicação;
* definir os modelos de entrada;
* carregar as regras;
* disponibilizar os endpoints;
* validar as requisições;
* executar a análise dos textos e documentos;
* retornar as respostas da API.

---

## `analisador.py`

Contém a lógica de análise de textos individuais.

Responsável por:

* normalizar o texto;
* verificar os fragmentos configurados;
* aplicar o critério da regra;
* identificar os itens encontrados.

---

## `analisador_processo.py`

Responsável pela análise dos documentos de um processo.

Para cada regra, verifica os conteúdos dos documentos e identifica os fragmentos correspondentes.

Quando uma regra é identificada, o processamento interno registra:

* identificador da regra;
* item;
* documento em que houve identificação;
* fragmento correspondente;
* trecho encontrado.

Essas informações são utilizadas internamente pela aplicação para determinar quais itens foram encontrados.

---

## `gerenciador_regras.py`

Responsável por:

* carregar o arquivo `regras.json`;
* validar a estrutura das regras;
* preparar as regras para utilização;
* normalizar os fragmentos;
* transformar os fragmentos em padrões de busca.

---

## `normalizador.py`

Responsável pela normalização dos textos utilizados durante as comparações.

A normalização permite que diferenças de:

* maiúsculas e minúsculas;
* acentuação;

não impeçam a identificação de um fragmento.

Por exemplo:

```text
Conferência
CONFERÊNCIA
conferencia
CONFERENCIA
```

podem ser tratados de forma equivalente durante a busca.

---

## `regras.json`

Arquivo que contém as regras utilizadas pela API.

As regras podem ser alteradas ou adicionadas sem necessidade de modificar a lógica principal da aplicação.

Cada regra possui, entre outras informações:

```json
{
  "id": "AP001",
  "item": "Nome do item",
  "ativo": true,
  "criterio": "qualquer",
  "fragmentos": [
    "fragmento 1",
    "fragmento 2"
  ]
}
```

Os identificadores seguem a convenção:

```text
AP001
AP002
AP003
...
```

O prefixo `AP` é utilizado independentemente do item ou categoria da regra.

---

# 5. Regras de identificação

As regras podem utilizar diferentes critérios.

## 5.1 Critério `qualquer`

Quando uma regra possui:

```json
"criterio": "qualquer"
```

o item é identificado quando **pelo menos um** dos fragmentos configurados for encontrado.

Exemplo:

```json
{
  "id": "AP004",
  "item": "Documento de identidade",
  "ativo": true,
  "criterio": "qualquer",
  "fragmentos": [
    "certidão de nascimento",
    "carteira de identidade",
    "carteira de motorista"
  ]
}
```

Nesse caso, a presença de qualquer um dos três fragmentos é suficiente para identificar o item.

---

## 5.2 Critério `todos`

Quando uma regra possui:

```json
"criterio": "todos"
```

todos os fragmentos configurados devem ser encontrados **no mesmo documento** para que a regra seja considerada identificada.

Exemplo:

```json
{
  "id": "AP005",
  "item": "Tempo Averbado",
  "ativo": true,
  "criterio": "todos",
  "fragmentos": [
    "INFORMAÇÕES COMPLEMENTARES À APOSENTADORIA",
    "TEMPO AVERBADO",
    "TEMPO DE SERVIÇO"
  ]
}
```

Se os três fragmentos estiverem no mesmo documento, o item é identificado.

Se os fragmentos estiverem distribuídos em documentos diferentes, o item não é considerado identificado.

---

# 6. Instalação local

Clone o repositório do projeto e entre na pasta:

```powershell
cd TextAnalyzerAPI
```

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

---

# 7. Executando a API localmente

Com o ambiente virtual ativado:

```powershell
python -m uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Para executar sem o modo de recarga automática:

```powershell
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

---

# 8. Documentação automática

O FastAPI disponibiliza documentação interativa automaticamente.

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

A documentação apresenta os endpoints e os modelos de entrada definidos pela aplicação.

---

# 9. Endpoint `/analisar`

## POST `/analisar`

Endpoint utilizado para analisar um texto individualmente.

Esse endpoint é útil para análises isoladas e testes da lógica de identificação.

---

## 9.1 Requisição

```json
{
  "texto": "O processo contém informações cadastrais do servidor."
}
```

---

## 9.2 Resposta quando um item é identificado

Exemplo:

```json
{
  "resultado": true,
  "motivo": "Itens identificados no texto.",
  "quantidade_itens": 1,
  "itens_encontrados": [
    {
      "id": "AP008",
      "item": "Dados Cadastrais"
    }
  ]
}
```

O campo `itens_encontrados` apresenta os itens identificados pela análise.

---

## 9.3 Resposta quando nenhum item é identificado

```json
{
  "resultado": false,
  "motivo": "Nenhum item previsto nas regras foi identificado no texto.",
  "quantidade_itens": 0,
  "itens_encontrados": []
}
```

---

## 9.4 Texto vazio

Quando o campo `texto` é informado, mas está vazio:

```json
{
  "texto": ""
}
```

Resposta:

```json
{
  "resultado": false,
  "motivo": "O texto informado está vazio.",
  "quantidade_itens": 0,
  "itens_encontrados": []
}
```

---

## 9.5 Campo `texto` não informado

Requisição:

```json
{}
```

Resposta:

```json
{
  "resultado": false,
  "motivo": "O campo 'texto' é obrigatório.",
  "quantidade_itens": 0,
  "itens_encontrados": []
}
```

---

# 10. Endpoint `/validar-processo`

## POST `/validar-processo`

Este é o principal endpoint destinado à integração com o sistema consumidor.

Recebe um processo e seus documentos e verifica se os itens previstos nas regras ativas foram identificados.

---

# 11. Estrutura da requisição

Exemplo:

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

---

## 11.1 Dados do processo

| Campo             | Tipo   | Descrição                        |
| ----------------- | ------ | -------------------------------- |
| `processo.numero` | string | Número identificador do processo |

---

## 11.2 Dados dos documentos

| Campo              | Tipo   | Descrição                                     |
| ------------------ | ------ | --------------------------------------------- |
| `data`             | string | Data do documento                             |
| `tipo`             | string | Tipo do documento                             |
| `numero`           | string | Número ou identificador do documento          |
| `conteudo`         | string | Conteúdo textual analisado pela API           |
| `assinaturas`      | lista  | Assinaturas associadas ao documento           |
| `content_type`     | string | Tipo de conteúdo do documento                 |
| `unidade_geradora` | string | Unidade responsável pela geração do documento |

---

## 11.3 Dados das assinaturas

| Campo  | Tipo   | Descrição         |
| ------ | ------ | ----------------- |
| `cpf`  | string | CPF do assinante  |
| `nome` | string | Nome do assinante |

---

# 12. Resposta do `/validar-processo`

A resposta desse endpoint foi projetada para ser simples para o sistema consumidor.

A resposta possui somente:

```text
resultado
itens_nao_encontrados
```

---

## 12.1 Processo completo

Quando todos os itens ativos das regras são identificados:

```json
{
  "resultado": true,
  "itens_nao_encontrados": []
}
```

O sistema consumidor pode interpretar:

```text
resultado = true
```

como:

> Todos os itens previstos pelas regras ativas foram identificados no processo.

---

## 12.2 Processo incompleto

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

O sistema consumidor pode interpretar:

```text
resultado = false
```

como:

> Existem itens previstos pelas regras ativas que não foram identificados no processo.

A lista `itens_nao_encontrados` informa quais itens precisam ser verificados pelo sistema consumidor.

---

# 13. Contrato de integração com o sistema consumidor

O sistema consumidor não precisa conhecer a implementação interna da API.

Para a integração, basta considerar a resposta do endpoint:

```text
POST /validar-processo
```

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

A lógica do sistema consumidor pode ser baseada diretamente no campo:

```text
resultado
```

Quando:

```text
resultado = false
```

o sistema pode consultar:

```text
itens_nao_encontrados
```

para saber quais itens não foram identificados.

---

# 14. Validação dos dados recebidos

A API utiliza Pydantic para validar a estrutura das requisições.

Por exemplo, o campo:

```text
texto
```

do endpoint `/analisar` deve ser uma string.

Da mesma forma, o endpoint `/validar-processo` espera a estrutura definida para:

```text
processo
documentos
assinaturas
```

Quando uma requisição não atende ao modelo esperado, a API pode retornar:

```text
HTTP 422 Unprocessable Entity
```

---

# 15. Testes automatizados

O projeto utiliza Pytest.

Para executar todos os testes:

```powershell
pytest
```

Para executar com informações mais detalhadas:

```powershell
pytest -v
```

Os testes abrangem:

* normalização de textos;
* identificação de fragmentos;
* critérios `qualquer` e `todos`;
* validação das regras;
* análise de documentos;
* endpoint `/analisar`;
* endpoint `/validar-processo`;
* validação dos modelos de entrada;
* utilização dos JSONs reais de processo.

---

# 16. Arquivos de teste com processos reais

O projeto possui arquivos utilizados como dados de teste:

```text
processo.json
processo 1.json
```

Esses arquivos representam estruturas reais de requisição utilizadas durante o desenvolvimento e a validação da API.

Eles são utilizados pelos testes automatizados para verificar o comportamento do endpoint:

```text
POST /validar-processo
```

---

# 17. Regras atuais

As regras utilizadas pela aplicação estão concentradas no arquivo:

```text
regras.json
```

Atualmente os identificadores seguem a sequência:

```text
AP001
AP002
AP003
AP004
AP005
AP006
AP007
AP008
AP009
```

Os itens e respectivos fragmentos devem ser alterados preferencialmente no arquivo `regras.json`, evitando alterações desnecessárias no código da aplicação.

---

# 18. Docker

A aplicação possui um `Dockerfile` para execução em container.

O container utiliza Python 3.14 e executa a aplicação através do Uvicorn.

## Construir a imagem

Na raiz do projeto:

```powershell
docker build -t textanalyzerapi .
```

---

## Executar o container

```powershell
docker run --name textanalyzerapi -p 8000:8000 textanalyzerapi
```

Após a inicialização, a API poderá ser acessada localmente em:

```text
http://127.0.0.1:8000
```

A documentação estará disponível em:

```text
http://127.0.0.1:8000/docs
```

---

## Executar o container em segundo plano

```powershell
docker run -d --name textanalyzerapi -p 8000:8000 textanalyzerapi
```

Para verificar os containers em execução:

```powershell
docker ps
```

Para visualizar os logs:

```powershell
docker logs textanalyzerapi
```

Para parar o container:

```powershell
docker stop textanalyzerapi
```

Para removê-lo:

```powershell
docker rm textanalyzerapi
```

---

# 19. Porta da aplicação

A aplicação utiliza a porta:

```text
8000
```

O container executa o Uvicorn com:

```text
0.0.0.0:8000
```

Isso permite que a aplicação receba conexões externas ao container.

Em ambientes de nuvem, como Azure, a infraestrutura deverá encaminhar a porta configurada para a aplicação conforme o serviço de hospedagem utilizado.

---

# 20. Arquitetura simplificada

O fluxo principal da validação pode ser representado da seguinte forma:

```text
Sistema consumidor
        |
        | HTTP POST
        v
/validar-processo
        |
        v
Validação do JSON
        |
        v
Carregamento das regras
        |
        v
Normalização dos textos
        |
        v
Análise dos documentos
        |
        v
Identificação dos itens
        |
        v
Comparação com regras ativas
        |
        v
Resposta simplificada
        |
        +----------------------+
        |                      |
        v                      v
resultado = true       resultado = false
        |                      |
        v                      v
lista vazia            itens não encontrados
```

---

# 21. Princípios da aplicação

A aplicação foi estruturada considerando:

* regras configuráveis;
* separação entre lógica de análise e contrato da API;
* normalização dos textos;
* validação das requisições;
* testes automatizados;
* possibilidade de execução local ou em container;
* integração simplificada com sistemas externos.

---

# 22. Execução recomendada para desenvolvimento

Para desenvolvimento local:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
python -m uvicorn main:app --reload
```

Depois, acessar:

```text
http://127.0.0.1:8000/docs
```

---

# 23. Execução recomendada para entrega

Para execução em ambiente de integração:

1. Construir a imagem Docker.
2. Executar os testes automatizados.
3. Validar a imagem localmente.
4. Disponibilizar a imagem ou o código-fonte para o ambiente de hospedagem.
5. Configurar a aplicação para utilizar a porta `8000`.
6. Utilizar o endpoint:

```text
POST /validar-processo
```

7. Utilizar a resposta:

```json
{
  "resultado": true,
  "itens_nao_encontrados": []
}
```

ou:

```json
{
  "resultado": false,
  "itens_nao_encontrados": [
    "Documento de identidade"
  ]
}
```

---

# 24. Repositório

O código-fonte do projeto está hospedado no GitHub.

O repositório utilizado durante o desenvolvimento é:

```text
diegovianasilvaGIT/TextAnalyzerAPI
```

---

# 25. Observação sobre evolução das regras

A inclusão, remoção ou alteração dos itens analisados deve ser realizada preferencialmente no arquivo:

```text
regras.json
```

Alterações nas regras devem ser acompanhadas da execução dos testes automatizados para garantir que o comportamento esperado da aplicação permaneça válido.

Quando uma alteração de regra modificar o comportamento esperado da API, os testes correspondentes também devem ser atualizados.

---

# 26. Resumo da interface de integração

### Endpoint

```text
POST /validar-processo
```

### Entrada

```json
{
  "processo": {
    "numero": "1500.01.0000000/2026-00"
  },
  "documentos": []
}
```

### Saída — processo completo

```json
{
  "resultado": true,
  "itens_nao_encontrados": []
}
```

### Saída — processo incompleto

```json
{
  "resultado": false,
  "itens_nao_encontrados": [
    "Documento de identidade",
    "Tempo Averbado"
  ]
}
```

O sistema consumidor pode utilizar diretamente esses dois campos para determinar se o processo possui todos os itens necessários identificados pelas regras ativas.
