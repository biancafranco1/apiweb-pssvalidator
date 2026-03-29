from typing import List
from app.models.classes import ResponseErrorDetails  


def validate_password(password:str) -> List[ResponseErrorDetails]:

    special_characters = {'!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+'}
    notvalid = []

    if len(password) < 9:
        notvalid.append({"rule": "minLenght", "message": "A senha deve conter pelo menos 9 catacteres"})
    if not any(char.isdigit() for char in password):
        notvalid.append({"rule": "number", "message": "A senha deve conter pelo menos 1 número"})
    if not any(char.islower() for char in password):
        notvalid.append({"rule": "lower", "message": "A senha deve conter pelo menos 1 letra minúscula"})
    if not any(char.isupper() for char in password):
        notvalid.append({"rule": "upper", "message": "A senha deve conter pelo menos 1 letra maiúscula"})
    if not any(char in set(special_characters) for char in password):
        notvalid.append({"rule": "symbol", "message": "A senha deve conter pelo menos 1 caractere especial"})
    if len(set(password)) != len (password):
        notvalid.append({"rule": "unique", "message": "A senha não pode conter caracteres duplicados"})
    if " " in password:
        notvalid.append({"rule": "space", "message": "A senha não deve conter espaços"})
    return notvalid