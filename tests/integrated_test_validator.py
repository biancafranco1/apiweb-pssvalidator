import pytest 
from utils.validate_password import validate_password
from tests.unit_test_validator import get_rules

class TestIntegration:
 
    def test_valid_password_returns_empty_list(self):
        """Senha 100% válida → lista de erros deve ser vazia."""
        pw = "Abcde1@!x"
        assert validate_password(pw) == []
 
    def test_all_rules_violated_simultaneously(self):
        """Edge case: senha que viola TODAS as regras ao mesmo tempo."""
        pw = "a a"  # curta, sem dígito, sem upper, sem symbol, com espaço, tem repetição de 'a' e ' '
        rules = get_rules(validate_password(pw))
        assert "minLenght" in rules
        assert "number"    in rules
        assert "upper"     in rules
        assert "symbol"    in rules
        assert "unique"    in rules
        assert "space"     in rules
 
    def test_multiple_rules_violated_returns_all(self):
        """Senha que viola 3 regras → deve retornar exatamente 3 erros."""
        pw = "abcdefgh1"  # sem upper, sem symbol → 2 regras; 9 chars → minLenght ok
        rules = get_rules(validate_password(pw))
        assert "upper"  in rules
        assert "symbol" in rules
        assert len(rules) == 2
 
    def test_result_contains_rule_and_message_keys(self):
        """Cada item do retorno deve ter as chaves 'rule' e 'message'."""
        pw = "abc"  # viola várias regras
        result = validate_password(pw)
        for item in result:
            assert "rule"    in item
            assert "message" in item
 
    def test_error_messages_are_strings(self):
        """As mensagens de erro devem ser strings não-vazias."""
        pw = "abc"
        result = validate_password(pw)
        for item in result:
            assert isinstance(item["message"], str)
            assert len(item["message"]) > 0
 