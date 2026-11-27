"""Testes do interpretador com programas INVÁLIDOS na semântica.
Categoria: erros semânticos. Todos passam pelo lexer e pelo parser; o erro
só aparece na execução.
Resultado esperado: todos levantam SemanticError ("Erro semântico: ..."),
e o programa para no comando que causou o erro."""
import pytest
from src.interpreter import executar_texto, SemanticError


def erro_de(texto):
    saida = []
    with pytest.raises(SemanticError) as e:
        executar_texto(texto, saida.append)
    return e.value, saida


# ---------- laços ----------

def test_while_com_condicao_nao_booleana():
    e, _ = erro_de("while (1 + 2) { print(1); }")
    assert "condição do 'while' deve ser booleana" in str(e)


def test_for_com_condicao_nao_booleana():
    e, _ = erro_de("for (i = 0; i + 1; i = i + 1) { }")
    assert "condição do 'for' deve ser booleana" in str(e)


def test_while_com_variavel_de_controle_nao_definida():
    e, _ = erro_de("while (k < 10) { k = k + 1; }")
    assert "'k'" in str(e) and "antes de ser definida" in str(e)


def test_for_com_variavel_nao_definida_na_condicao():
    e, _ = erro_de("for (i = 0; j < 10; i = i + 1) { }")
    assert "'j'" in str(e)


def test_for_com_variavel_nao_definida_na_inicializacao():
    e, _ = erro_de("for (i = n; i < 10; i = i + 1) { }")
    assert "'n'" in str(e)


# ---------- demais erros semânticos ----------

def test_if_com_condicao_nao_booleana():
    e, _ = erro_de("if (1) { print(1); }")
    assert "'if'" in str(e)


def test_variavel_nao_definida():
    e, _ = erro_de("x = y + 1;")
    assert "'y'" in str(e) and "antes de ser definida" in str(e)


def test_divisao_por_zero():
    e, _ = erro_de("x = 1 / (2 - 2);")
    assert "divisão por zero" in str(e)


def test_soma_de_booleano_com_inteiro():
    # Em Python, True + 1 daria 2. Na MiniLang é erro de tipo.
    e, _ = erro_de("x = true + 1;")
    assert "exige inteiros" in str(e)


def test_comparacao_de_ordem_entre_booleanos():
    e, _ = erro_de("x = true < false;")
    assert "exige inteiros" in str(e)


def test_igualdade_entre_tipos_diferentes():
    # Em Python, 1 == True daria True. Na MiniLang é erro de tipo.
    e, _ = erro_de("x = 1 == true;")
    assert "não compara" in str(e)


def test_erro_interrompe_a_execucao_no_ponto_do_erro():
    e, saida = erro_de("print(1); x = z; print(2);")
    assert saida == ["1"]
