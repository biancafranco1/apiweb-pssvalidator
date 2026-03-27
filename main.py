
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Union

app = FastAPI()

class PasswordRequest(BaseModel):
    password:str

class PasswordResponse(BaseModel):
    valid: bool
    notvalid: Union[List[str],str]

def validate_password(password:str) -> List[str]:

    special_characters = {'!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+'}
    notvalid = []

    if len(password) < 9:
        notvalid.append('A senha é muito curta. Mínimo: 9 caracteres.')
    if not any(char.isdigit() for char in password):
        notvalid.append('A senha precisa conter pelo menos 1 número')
    if not any(char.islower() for char in password):
        notvalid.append('A senha precisa conter pelo menos 1 letra minuscula')
    if not any(char.isupper() for char in password):
        notvalid.append('A senha precisa conter pelo menos 1 letra maiúscula')
    if not any(char in list(special_characters) for char in password):
        notvalid.append('A senha precisa conter pelo menos 1 caractere especial')
    if len(set(password)) != len (password):
        notvalid.append('A senha não pode conter caracteres duplicados')
    if " " in password:
        notvalid.append('A senha não pode conter espaço')
    return notvalid

@app.post("/user/validate", status_code=status.HTTP_201_CREATED ,response_model=PasswordResponse)
async def validation_pss(request: PasswordRequest):
    try:
        #test = 123
        #test.islower()
        notvalid = validate_password(request.password)
        if notvalid:
            return PasswordResponse(valid=False, notvalid=notvalid)
        return PasswordResponse(valid=True, notvalid='null')
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"An internal error occurred"}
        )


#Ajustar os caracteres especiais para conjunto para funcionar o retorno json- ok
#Como no fastapi devolve o status code 
#Return estruturado em json ao inves de string - com camadas: Valid = True / False + details: o que faltou para estar certo
# Cenários de testes - Status code para validação
#Formas de não percorrer tudo seria ver a string completa já fazendo as validações letra por letra
#Separar a def e o servidor de pasta para melhorar acoplamento e extensibilidade
#Boas práticas de API Rest - como devolve e recebe os dados

