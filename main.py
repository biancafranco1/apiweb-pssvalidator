#Critérios:
# 9 ou mais caracteres
# Pelo menos um número, uma letra maiuscula, 1 letra minuscula e 1 caractere especial
# Não possuir números repetidos no conjunto

senha = 'Abcdefgh9@'
caracteres_especiais = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+']

def valida_senha(senha:str) -> bool:
    if len(senha) < 9:
        print('A senha é muito curta')
        return False
    if not any(char.isdigit() for char in senha):
        print('senha precisa conter pelo menos 1 número')
        return False
    if not any(char.islower() for char in senha):
        print('senha precisa conter pelo menos 1 letra minuscula')
        return False
    if not any(char.isupper() for char in senha):
        print('senha precisa conter pelo menos 1 letra maiúscula')
        return False
    if not any(char in list(caracteres_especiais) for char in senha):
        print('senha precisa conter pelo menos 1 caractere especial')
        return False
    if len(set(senha)) != len (senha):
        print('senha não pode conter caracteres duplicados')
        return False
    if " " in senha:
        print('senha não pode conter espaço')
        return False
    print('senha ok')
    return True

valida_senha(senha)
