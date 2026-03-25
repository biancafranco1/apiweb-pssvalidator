#Critérios:
# 9 ou mais caracteres
# Pelo menos um número, uma letra maiuscula, 1 letra minuscula e 1 caractere especial
# Não possuir números repetidos no conjunto

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union

special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+']
app = FastAPI()

class PasswordRequest(BaseModel):
    Password:str


def password_rules(Password:str) -> bool:
    if len(Password) < 9:
        print('A senha é muito curta')
        return False
    if not any(char.isdigit() for char in Password):
        print('senha precisa conter pelo menos 1 número')
        return False
    if not any(char.islower() for char in Password):
        print('senha precisa conter pelo menos 1 letra minuscula')
        return False
    if not any(char.isupper() for char in Password):
        print('senha precisa conter pelo menos 1 letra maiúscula')
        return False
    if not any(char in list(special_characters) for char in Password):
        print('senha precisa conter pelo menos 1 caractere especial')
        return False
    if len(set(Password)) != len (Password):
        print('senha não pode conter caracteres duplicados')
        return False
    if " " in Password:
        print('senha não pode conter espaço')
        return False
    print('senha ok')
    return True

@app.post("/user/validate")
async def validation_pss(request: PasswordRequest):
    return {"Password": request.Password}

