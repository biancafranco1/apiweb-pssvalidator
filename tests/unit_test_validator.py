import pytest 
from app.services.validate_password import validate_password
from typing import List


def get_rules(result: List[dict]) -> List[str]:
    """Extrai apenas os nomes das regras violadas."""
    return [item["rule"] for item in result]
 
 
def assert_rule_triggered(password: str, rule: str):
    """Garante que a regra foi disparada."""
    assert rule in get_rules(validate_password(password)), (
        f"Esperava que a regra '{rule}' fosse disparada para a senha: {password!r}"
    )
 
 
def assert_rule_not_triggered(password: str, rule: str):
    """Garante que a regra NÃO foi disparada."""
    assert rule not in get_rules(validate_password(password)), (
        f"Não esperava que a regra '{rule}' fosse disparada para a senha: {password!r}"
    )
 
 
#  REGRA: minLenght  (mínimo 9 caracteres)
class TestMinLength:
    RULE = "minLenght"
 
    def test_8_chars_triggers_rule(self):
        """1 caractere a menos do mínimo → deve falhar."""
        # 8 chars, todas as outras regras satisfeitas
        pw = "Abcde1@x"          # 8 chars
        assert_rule_triggered(pw, self.RULE)
 
    def test_9_chars_passes_rule(self):
        """Exatamente no limite mínimo → deve passar."""
        pw = "Abcde1@xy"         # 9 chars
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_10_chars_passes_rule(self):
        """1 caractere a mais do mínimo → deve passar."""
        pw = "Abcde1@xyz"        # 10 chars
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_1_char_triggers_rule(self):
        """Edge case: senha de 1 único caractere."""
        pw = "A"
        assert_rule_triggered(pw, self.RULE)
 
    def test_empty_string_triggers_rule(self):
        """Edge case: string vazia."""
        pw = ""
        assert_rule_triggered(pw, self.RULE)

#  REGRA: number  (pelo menos 1 dígito)
class TestNumber:
    RULE = "number"
 
    def test_no_digit_triggers_rule(self):
        """Nenhum dígito → deve falhar."""
        pw = "Abcdefg@!"
        assert_rule_triggered(pw, self.RULE)
 
    def test_one_digit_passes_rule(self):
        """Exatamente 1 dígito → deve passar."""
        pw = "Abcdefg1@"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_multiple_digits_passes_rule(self):
        """Mais de 1 dígito → deve passar."""
        pw = "Abcde123@"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_digit_at_start_passes_rule(self):
        """Dígito na primeira posição → deve passar."""
        pw = "1Abcdefg@"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_digit_at_end_passes_rule(self):
        """Edge case: dígito apenas no final."""
        pw = "Abcdefg@2"
        assert_rule_not_triggered(pw, self.RULE)
 

#  REGRA: lower  (pelo menos 1 letra minúscula)
class TestLower:
    RULE = "lower"
 
    def test_no_lowercase_triggers_rule(self):
        """Nenhuma minúscula → deve falhar."""
        pw = "ABCDE12@!"
        assert_rule_triggered(pw, self.RULE)
 
    def test_one_lowercase_passes_rule(self):
        """Exatamente 1 minúscula → deve passar."""
        pw = "ABCDEa2@!"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_all_lowercase_passes_rule(self):
        """Todas minúsculas (+ obrigatórios) → deve passar a regra lower."""
        pw = "abcde12@!"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_lowercase_in_middle_passes_rule(self):
        """Minúscula no meio da senha → deve passar."""
        pw = "ABCaDE2@!"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_only_digits_and_symbols_triggers_rule(self):
        """Edge case: apenas números e símbolos, sem letra alguma."""
        pw = "12345678@!"
        assert_rule_triggered(pw, self.RULE)
 

#  REGRA: upper  (pelo menos 1 letra maiúscula)
class TestUpper:
    RULE = "upper"
 
    def test_no_uppercase_triggers_rule(self):
        """Nenhuma maiúscula → deve falhar."""
        pw = "abcde12@!"
        assert_rule_triggered(pw, self.RULE)
 
    def test_one_uppercase_passes_rule(self):
        """Exatamente 1 maiúscula → deve passar."""
        pw = "abcdeA2@!"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_all_uppercase_passes_rule(self):
        """Todas maiúsculas (+ obrigatórios) → deve passar a regra upper."""
        pw = "ABCDE12@!"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_uppercase_at_end_passes_rule(self):
        """Maiúscula apenas no final → deve passar."""
        pw = "abcde12@Z"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_only_digits_and_symbols_triggers_rule(self):
        """Edge case: apenas números e símbolos, sem letra alguma."""
        pw = "12345678@!"
        assert_rule_triggered(pw, self.RULE)
 

#  REGRA: symbol  (pelo menos 1 caractere especial)
class TestSymbol:
    RULE = "symbol"
    VALID_SYMBOLS = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+']
 
    def test_no_symbol_triggers_rule(self):
        """Nenhum símbolo especial → deve falhar."""
        pw = "Abcde123x"
        assert_rule_triggered(pw, self.RULE)
 
    def test_each_valid_symbol_passes_rule(self):
        """Cada símbolo válido individualmente → deve passar."""
        for sym in self.VALID_SYMBOLS:
            pw = f"Abcde1{sym}xy"
            assert_rule_not_triggered(pw, self.RULE)
 
    def test_symbol_not_in_set_triggers_rule(self):
        """Símbolo fora do conjunto permitido (ex: '~') → deve falhar."""
        pw = "Abcde12~x"
        assert_rule_triggered(pw, self.RULE)
 
    def test_multiple_valid_symbols_passes_rule(self):
        """Mais de um símbolo válido → deve passar."""
        pw = "Abcde1@#x"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_symbol_at_start_passes_rule(self):
        """Edge case: símbolo na primeira posição → deve passar."""
        pw = "@Abcde12x"
        assert_rule_not_triggered(pw, self.RULE)
 

#  REGRA: unique  (sem caracteres repetidos)
class TestUnique:
    RULE = "unique"
 
    def test_repeated_letter_triggers_rule(self):
        """Letra repetida → deve falhar."""
        pw = "Aabcda1@!"   # 'a' minúsculo aparece em posição 1 e 5
        assert_rule_triggered(pw, self.RULE)
 
    def test_all_unique_chars_passes_rule(self):
        """Todos os caracteres distintos → deve passar."""
        pw = "Abcde1@!"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_repeated_digit_triggers_rule(self):
        """Dígito repetido → deve falhar."""
        pw = "Abcde11@!"
        assert_rule_triggered(pw, self.RULE)
 
    def test_repeated_symbol_triggers_rule(self):
        """Símbolo especial repetido → deve falhar."""
        pw = "Abcde1@@x"
        assert_rule_triggered(pw, self.RULE)
 
    def test_all_same_char_triggers_rule(self):
        """Edge case: todos os caracteres iguais."""
        pw = "AAAAAAAAA"
        assert_rule_triggered(pw, self.RULE)
 

#  REGRA: space  (sem espaços)
class TestSpace:
    RULE = "space"
 
    def test_space_in_middle_triggers_rule(self):
        """Espaço no meio da senha → deve falhar."""
        pw = "Abcde 1@!"
        assert_rule_triggered(pw, self.RULE)
 
    def test_no_space_passes_rule(self):
        """Sem nenhum espaço → deve passar."""
        pw = "Abcde1@!x"
        assert_rule_not_triggered(pw, self.RULE)
 
    def test_space_at_start_triggers_rule(self):
        """Espaço no início da senha → deve falhar."""
        pw = " Abcde1@!"
        assert_rule_triggered(pw, self.RULE)
 
    def test_space_at_end_triggers_rule(self):
        """Espaço no final da senha → deve falhar."""
        pw = "Abcde1@! "
        assert_rule_triggered(pw, self.RULE)
 
    def test_multiple_spaces_triggers_rule(self):
        """Edge case: múltiplos espaços → deve falhar."""
        pw = "Ab de 1@!"
        assert_rule_triggered(pw, self.RULE)
 
