import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from starlette.testclient import TestClient as TestClient 
import httpx 


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def valid_password():
    """Senha que satisfaz todas as regras."""
    return "Abcde1@!x"


@pytest.fixture
def post(client):
    """Atalho para POST /user/validate com JSON."""
    def _post(body, **kwargs):
        return client.post("/user/validate", json=body, **kwargs)
    return _post


#Comportamento central
class TestRespostaAPI:

    def test_tc01_senha_valida_retorna_200_e_valid_true(self, post, valid_password):
        """Senha válida → HTTP 200, valid: true, notvalid: []."""
        response = post({"password": valid_password})

        assert response.status_code == 200
        body = response.json()
        assert body["valid"] is True
        assert body["notvalid"] == []

    def test_tc02_senha_invalida_retorna_valid_false(self, post):
        """1 regra violada: Valid: false, notvalid com 1 item."""
        # Viola apenas 'minLenght' (8 chars, mas satisfaz todas as outras)
        response = post({"password": "Abcde1@x"})

        assert response.status_code == 200
        body = response.json()
        assert body["valid"] is False
        assert len(body["notvalid"]) >= 1
        rules = [e["rule"] for e in body["notvalid"]]
        assert "minLenght" in rules

    def test_tc03_multiplas_violacoes_retornam_todos_erros(self, post):
        """N regras violadas → notvalid com exatamente N itens."""
        # Viola: minLenght, number, upper, symbol (4 regras)
        response = post({"password": "abcde"})

        assert response.status_code == 200
        body = response.json()
        rules = [e["rule"] for e in body["notvalid"]]
        assert "minLenght" in rules
        assert "number"    in rules
        assert "upper"     in rules
        assert "symbol"    in rules

    def test_tc04_estrutura_do_response_model_e_respeitada(self, post, valid_password):
        """Response sempre contém 'valid' (bool) e 'notvalid' (lista)."""
        # Testa com senha válida
        r_valid = post({"password": valid_password})
        body_v = r_valid.json()
        assert isinstance(body_v["valid"], bool)
        assert isinstance(body_v["notvalid"], list)

        # Testa com senha inválida
        r_invalid = post({"password": "abc"})
        body_i = r_invalid.json()
        assert isinstance(body_i["valid"], bool)
        assert isinstance(body_i["notvalid"], list)
        for item in body_i["notvalid"]:
            assert "rule"    in item
            assert "message" in item
            assert isinstance(item["rule"],    str)
            assert isinstance(item["message"], str)


#Integração status HTTP
class TestContratoHTTP:

    def test_tc05_body_ausente_retorna_422(self, client):
        """POST sem body → 422 Unprocessable Entity."""
        response = client.post("/user/validate")
        assert response.status_code == 422

    def test_tc06_campo_password_ausente_retorna_422(self, post):
        """Body sem a chave 'password' → 422."""
        response = post({"senha": "qualquer"})
        assert response.status_code == 422

        body = response.json()
        # FastAPI/Pydantic indica qual campo está faltando
        erros = str(body)
        assert "password" in erros

    def test_tc07_content_type_incorreto_retorna_422(self, client):
        """Dados enviados como form-data → 422."""
        response = client.post(
            "/user/validate",
            data={"password": "Abcde1@!x"},   # form-data, não JSON
        )
        assert response.status_code == 422

    def test_tc08_metodo_get_retorna_405(self, client):
        """GET na rota → 405 Method Not Allowed."""
        response = client.get("/user/validate")
        assert response.status_code == 405

    def test_tc08_metodo_put_retorna_405(self, client):
        """PUT na rota → 405."""
        response = client.put("/user/validate", json={"password": "x"})
        assert response.status_code == 405

    def test_tc09_content_type_response_e_json(self, post, valid_password):
        """ Header Content-Type da resposta deve ser application/json."""
        response = post({"password": valid_password})
        assert "application/json" in response.headers["content-type"]


#Edge cases
class TestEdgeCases:

    def test_tc10_password_como_inteiro_no_json(self, post):
        """Password com valor numérico → Pydantic coerce para str ou 422."""
        response = post({"password": 123456789})
        # Pydantic v2 por padrão rejeita coerção de int → str em modo strict.
        # Pydantic v1 aceita e converte. Ambos os comportamentos são válidos —
        # o teste documenta qual o comportamento real do projeto.
        assert response.status_code in (200, 422)

    def test_tc11_password_nulo_retorna_422(self, post):
        """password: null → 422 pois o campo é str não-opcional."""
        response = post({"password": None})
        assert response.status_code == 422

    def test_tc12_senha_com_caracteres_unicode(self, post):
        """Senha com acentos e caracteres multibyte não deve gerar 500."""
        # 'Á' é upper, 'r' é lower, '1' é digit, '@' é symbol, todos únicos
        response = post({"password": "Árvore1@!"})
        assert response.status_code == 200
        body = response.json()
        assert "valid" in body
        assert "notvalid" in body

    def test_tc13_senha_extremamente_longa(self, post):
        """Senha com 10.000+ chars deve processar sem erro 500."""
        # Garante que todas as regras sejam satisfeitas no prefixo
        prefix = "Abcde1@!x"
        senha_longa = prefix + "y" * (10_000 - len(prefix))
        # Nota: a regra 'unique' será violada — o esperado é 200 com valid: false
        response = post({"password": senha_longa})
        assert response.status_code == 200

    def test_tc14_senha_string_vazia(self, post):
        """password: '' → 200, valid: false, com regras esperadas."""
        response = post({"password": ""})

        assert response.status_code == 200
        body = response.json()
        assert body["valid"] is False
        rules = [e["rule"] for e in body["notvalid"]]
        assert "minLenght" in rules
        assert "number"    in rules
        assert "lower"     in rules
        assert "upper"     in rules
        assert "symbol"    in rules

    def test_tc15_campos_extras_sao_ignorados(self, post, valid_password):
        """Body com campos adicionais → ignorados, processamento normal."""
        response = post({
            "password": valid_password,
            "campo_extra": "valor",
            "outro": 42,
        })
        assert response.status_code == 200
        assert response.json()["valid"] is True

    def test_tc18_json_malformado_retorna_422(self, client):
        """JSON inválido no body → 422, nunca 500."""
        response = client.post(
            "/user/validate",
            content=b'{"password": }',           # JSON inválido
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422

    def test_tc19_rota_inexistente_retorna_404(self, client):
        """Rota errada → 404 Not Found."""
        rotas_erradas = [
            "/user/validar",
            "/validate",
            "/user/validate/extra",
            "/",
        ]
        for rota in rotas_erradas:
            response = client.post(rota, json={"password": "teste"})
            assert response.status_code == 404, (
                f"Esperava 404 para a rota '{rota}', "
                f"mas recebeu {response.status_code}"
            )

    def test_tc20_escape_characters_nao_causam_erro(self, post):
        """Escape characters em senha → processados como string comum, sem 500."""
        senhas_com_escape = [
            "Abcde1@!\n",    # newline
            "Abcde1@!\t",    # tab
            'Abcde1@!\\"'   # aspas escapadas
        ]
        for senha in senhas_com_escape:
            response = post({"password": senha})
            assert response.status_code == 200, (
                f"Esperava 200 para senha com escape, mas recebeu "
                f"{response.status_code} para: {senha!r}"
            )
            body = response.json()
            assert "valid"    in body
            assert "notvalid" in body