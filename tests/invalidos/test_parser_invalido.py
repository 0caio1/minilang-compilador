"""Testes do parser com entradas INVÁLIDAS.
Resultado esperado: todas levantam ParseError, com a posição do problema."""
from pathlib import Path

import pytest
from src.parser import analisar_texto, ParseError

RAIZ = Path(__file__).resolve().parents[2]


def erro_de(texto):
    with pytest.raises(ParseError) as e:
        analisar_texto(texto)
    return e.value


def test_expressao_incompleta():
    e = erro_de("x = (1 + ;")
    assert "esperada uma expressão" in str(e)
    assert (e.linha, e.coluna) == (1, 10)


def test_falta_ponto_e_virgula():
    e = erro_de("x = 1\ny = 2;")
    assert "';'" in str(e)
    assert e.linha == 2


def test_for_sem_clausula_de_atualizacao():
    e = erro_de("for (i = 0; i < 10) { print(i); }")
    assert "atualização" in str(e)
    assert (e.linha, e.coluna) == (1, 19)


def test_for_com_clausulas_vazias():
    e = erro_de("for (;;) { print(1); }")
    assert "inicialização" in str(e)


def test_for_sem_condicao():
    e = erro_de("for (i = 0; ; i = i + 1) { }")
    assert "condição" in str(e)


def test_for_com_inicializacao_que_nao_e_atribuicao():
    e = erro_de("for (0; i < 3; i = i + 1) { }")
    assert "inicialização" in str(e)


def test_while_sem_parenteses():
    e = erro_de("while x > 0 { x = x - 1; }")
    assert "'('" in str(e)


def test_while_sem_bloco():
    e = erro_de("while (x > 0) x = x - 1;")
    assert "'{'" in str(e)


def test_bloco_nao_fechado():
    e = erro_de("while (x > 0) {\n  x = x - 1;\n")
    assert "não foi fechado" in str(e)


def test_comparacao_encadeada():
    e = erro_de("x = 1 < 2 < 3;")
    assert "não são associativos" in str(e)


def test_else_sem_if():
    e = erro_de("else { print(1); }")
    assert "'else' sem 'if'" in str(e)


def test_print_sem_parenteses():
    erro_de("print x;")


def test_menos_unario_nao_existe_na_gramatica():
    erro_de("x = -1;")


def test_programa_invalido_de_exemplo():
    texto = (RAIZ / "exemplos" / "programa_invalido.ml").read_text(encoding="utf-8")
    e = erro_de(texto)
    assert e.linha == 2
