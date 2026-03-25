
# Password Validator

## Objetivos do projeto
Desafio backend desenvolvido com objetivo de criar uma API web que realize a validação de critérios de aceite para criação de senha.

## Funcionalidades Implementadas


## Tecnologias utilizadas
- Python 3.12.3
- FastAPI

Ferramentas adicionais: 
- Postman como client HTTP

Cenário de testes:
- Unidade e integração - A decidir

## Documentação de uso da API
Para subir o servidor:  uvicorn main:app --reload
Para testar a Requisição no terminal: 
    
    ```
    curl -X POST http://127.0.0.1:8000/user/validate (Substituir a porta que retornou na subida do servidor se necessário)
    -H "Content-Type: application/json" 
    -d '{"senha": "Senh@1234"}'
    ```
Retorno esperado: HTTP Status 200


## Fundamentação das decisões

- Flask x FastAPI
Embora a biblioteca Flask fosse mais simples e não utilizasse tipagem, nesse projeto foi considerado o uso do FastAPI por conta da possibilidade do uso da integração dos cenários de testes com Pydantic e a possibilidade de apoio na construção de partes da documentação de maneira automática.

- Lista x String dos caracteres especiais
String é imutável e lista permite substituições