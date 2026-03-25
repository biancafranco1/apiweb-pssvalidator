
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

## Fundamentação das decisões

- Flask x FastAPI
Embora a biblioteca Flask fosse mais simples e não utilizasse tipagem, nesse projeto foi considerado o uso do FastAPI por conta da possibilidade do uso da integração dos cenários de testes com Pydantic e a possibilidade de apoio na construção de partes da documentação de maneira automática.

- Lista x String 
String é imutável e lista permite substituições