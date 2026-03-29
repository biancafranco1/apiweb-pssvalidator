# 🔐 Password Validator API

API web desenvolvida em Python com FastAPI para validação de critérios de aceite na criação de senhas.

---

## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Como Executar](#como-executar)
- [Documentação da API](#documentação-da-api)
- [Exemplos de Uso](#exemplos-de-uso)
- [Testes](#testes)
- [Decisões Técnicas e racional das decisões](#decisões-técnicas)

---

## Sobre o Projeto

Desafio backend desenvolvido com o objetivo de criar uma API web que realize a validação de critérios de aceite para criação de senha. A API recebe uma senha e retorna se ela é válida ou não, acompanhada de uma lista das regras que foram violadas para possibilitar a correção por parte do usuário.

### Regras de validação implementadas

| Regra | Descrição |
|---|---|
| `minLength` | A senha deve ter no mínimo 9 caracteres |
| `number` | A senha deve conter pelo menos 1 número |
| `lower` | A senha deve conter pelo menos 1 letra minúscula |
| `upper` | A senha deve conter pelo menos 1 letra maiúscula |
| `symbol` | A senha deve conter pelo menos 1 caractere especial (`! @ # $ % ^ & * ( ) - +`) |
| `unique` | A senha não pode conter caracteres duplicados |
| `space` | A senha não deve conter espaços |

---

## Tecnologias Utilizadas

- **[Python 3.12.3](https://www.python.org/)** — Linguagem principal
- **[FastAPI 0.135.2](https://fastapi.tiangolo.com/)** — Framework web
- **[Pydantic 2.12.5](https://docs.pydantic.dev/)** — Validação e serialização de dados
- **[Uvicorn 0.42.0](https://www.uvicorn.org/)** — Servidor ASGI
- **[Pytest 9.0.2](https://docs.pytest.org/)** — Framework de testes
- **[HTTPx 0.28.1](https://www.python-httpx.org/)** — Cliente HTTP para testes de integração

**Ferramentas adicionais:**
- [Postman](https://www.postman.com/) — Client HTTP para teste manual dos endpoints

---

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- [Python 3.12+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)

---

## Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/biancafranco1/apiweb-pssvalidator.git
cd apiweb-pssvalidator
```

### 2. Crie e ative um ambiente virtual

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar no Linux/macOS
source venv/bin/activate

# Ativar no Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie o servidor

```bash
uvicorn main:app --reload
```

O servidor estará disponível em: **`http://127.0.0.1:8000`**

> A flag `--reload` faz o servidor reiniciar automaticamente ao detectar alterações no código. Recomendada apenas em desenvolvimento.

### 5. Acesse a documentação interativa

O FastAPI gera automaticamente duas interfaces de documentação:

| Interface | URL |
|---|---|
| Swagger UI | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| Redoc | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc1) |

---

## Documentação da API

### Base URL

```
http://127.0.0.1:8000
```

---

### `POST /user/validate`

Valida se uma senha atende a todos os critérios de segurança exigidos.

#### Request

**Headers**

```
Content-Type: application/json
```

**Body**

```json
{
  "password": "string"
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `password` | `string` | ✅ Sim | A senha a ser validada |

#### Response

**`200 OK`** — Requisição processada com sucesso (senha válida ou inválida)

```json
{
  "valid": true,
  "notvalid": []
}
```

```json
{
  "valid": false,
  "notvalid": [
    {
      "rule": "string",
      "message": "string"
    }
  ]
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| `valid` | `boolean` | `true` se a senha atende a todos os critérios, `false` caso contrário |
| `notvalid` | `array` | Lista das regras violadas. Vazia quando a senha é válida |
| `notvalid[].rule` | `string` | Identificador da regra violada |
| `notvalid[].message` | `string` | Mensagem descritiva da violação |

**`500 Internal Server Error`** — Erro inesperado no processamento

```json
{
  "message": "Ocorreu um erro de processamento no servidor"
}
```

---

## Exemplos de Uso

### Senha válida

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/user/validate \
  -H "Content-Type: application/json" \
  -d '{"password": "TesteSen#1"}'
```

**Response (`200 OK`):**
```json
{
  "valid": true,
  "notvalid": []
}
```

---

### Senha inválida (múltiplas violações)

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/user/validate \
  -H "Content-Type: application/json" \
  -d '{"password": "senha"}'
```

**Response (`200 OK`):**
```json
{
  "valid": false,
  "notvalid": [
    {
      "rule": "minLength",
      "message": "A senha deve conter pelo menos 9 caracteres"
    },
    {
      "rule": "number",
      "message": "A senha deve conter pelo menos 1 número"
    },
    {
      "rule": "upper",
      "message": "A senha deve conter pelo menos 1 letra maiúscula"
    },
    {
      "rule": "symbol",
      "message": "A senha deve conter pelo menos 1 caractere especial"
    }
  ]
}
```

---

### Senha com caracteres duplicados

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/user/validate \
  -H "Content-Type: application/json" \
  -d '{"password": "AaBb@1233"}'
```

**Response (`200 OK`):**
```json
{
  "valid": false,
  "notvalid": [
    {
      "rule": "unique",
      "message": "A senha não pode conter caracteres duplicados"
    }
  ]
}
```

---

## Testes

Os cenários de testes incluem testes de unidade e integração.

Para executar com saída detalhada:

```bash
pytest -v tests/<arquivo de teste desejado>.py
```

Exemplos:
- pytest - v tests/integrated_test_api.py
- pytest - v tests/integrated_test_validator.py
- pytest - v tests/unit_test_validator.py

---

## Decisões Técnicas e racional das decisões 

### Escolha da linguagem Python

A escolha da linguagem Python foi feita por familiaridade pelo contato em outros projetos e sintaxe facilitada da própria linguagem, visando a resolução de possíveis desafios que pudessem aparecer durante o desenvolvimento da API e viabilizasse o estudado durante o desenvolvimento do projeto visando respeitar a data de entrega e critérios de aceite que foram estabelecidos.

### Escolha do uso e quais bibliotecas: Flask x FastAPI

Embora o Flask seja mais simples e não exija tipagem, neste projeto optei pelo **FastAPI** pelos seguintes motivos:
- Integração nativa com **Pydantic** para validação de dados e apoio na escrita de testes
- Geração automática de documentação interativa via **Swagger UI** e **Redoc**
- Suporte a tipagem estática com Python type 
- Alta performance via Uvicorn 

### Escolha do nome user/validator para o endpoint

Essa escolha foi baseada em materiais de boas práticas para nomenclatura, que sugere nomes simples e intuitivos aos endpoints. Neste caso com a particularidade de trafegar senhas, o desafio foi deixar simples, intuitivo mas sem exposição, por isso evitei o uso das palavras: senha, password, pss, entre outras que pudessem evidenciar o conteúdo.

### Devolução do response em forma estruturada e identificada por chaves

Embora o desafio propusesse o retorno em boolean, decidi adicionar uma mensagem de erro e a possibilidade deles se agregarem em um objeto que retorna todos as regras de senha que foram infringidas. 
Essa escolha foi pensando no consumo da API pelo Frontend onde neste caso as mensagens podem ser melhoradas e expostas, ou até mesmo na ausência de um front diretamente ao usuário final para que possibilite a correção e melhore a UX.

### Uso de IA

A construção da lógica e seu funcionamento foi propositalmente escrita manualmente por se tratar de um teste para validação de conhecimento. Para a construção do projeto me apoiei em pesquisas, documentações oficiais e fóruns o que naturalmente ocasionou um processo evolutivo nas features do projeto.
Embora reconheça o valor e o ganho em agilidade do uso de IA bem utilizada, quis evidenciar meus conhecimentos próprios e adquirir novos durante o processo, por isso reservei o uso de IA para operações menos racionais e mais repetitivas, como:
- Apoio na escrita dos casos de testes, após instruções do que deveria ser verificado e validado;
- Apoio em debugg de erros;
- Melhoria da documentação de uso do produto. 

Todas as etapas priorizando a validação de tudo o que foi feito pela IA, melhorias e correções quando necessárias e aproveitamento de aprendizagem.
Entendo que há oportunidades para utilização e refatoração dos códigos visando melhoria de performance e agilidade na construção em cenários do dia a dia.



