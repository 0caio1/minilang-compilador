"""Testes do lexer com entradas INVÁLIDAS.
Resultado esperado: todas levantam LexError, com a posição do problema."""
import pytest
from src.lexer import tokenizar, LexError


def test_caractere_invalido_arroba():
    with pytest.raises(LexError) as e:
        tokenizar("x = @;")
    assert "caractere inválido" in str(e.value)
    assert (e.value.linha, e.value.coluna) == (1, 5)


def test_identificador_comecando_com_digito():
    with pytest.raises(LexError) as e:
        tokenizar("1x = 5;")
    assert "dígito" in str(e.value)


def test_comentario_de_bloco_nao_fechado():
    with pytest.raises(LexError) as e:
        tokenizar("x = 1; /* sem fim")
    assert "não fechado" in str(e.value)
    assert (e.value.linha, e.value.coluna) == (1, 8)


def test_exclamacao_sozinha():
    with pytest.raises(LexError):
        tokenizar("x ! y")


def test_cifrao():
    with pytest.raises(LexError):
        tokenizar("$a = 1;")
