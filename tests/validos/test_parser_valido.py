"""Testes do parser com entradas VÁLIDAS.
Resultado esperado: cada entrada gera exatamente a AST indicada."""
from pathlib import Path

from src.parser import analisar_texto
from src.ast_nodes import (Num, Bool, Var, BinOp, Atribuicao, Print, Bloco,
                           If, While, For, Programa)

RAIZ = Path(__file__).resolve().parents[2]


def expr(texto):
    return analisar_texto(f"x = {texto};").comandos[0].expr


def test_precedencia_multiplicacao_antes_da_soma():
    assert expr("1 + 2 * 3") == BinOp("+", Num(1), BinOp("*", Num(2), Num(3)))


def test_parenteses_mudam_a_arvore():
    assert expr("(1 + 2) * 3") == BinOp("*", BinOp("+", Num(1), Num(2)), Num(3))


def test_subtracao_associativa_a_esquerda():
    assert expr("10 - 3 - 2") == BinOp("-", BinOp("-", Num(10), Num(3)), Num(2))


def test_divisao_associativa_a_esquerda():
    assert expr("8 / 4 / 2") == BinOp("/", BinOp("/", Num(8), Num(4)), Num(2))


def test_comparacao_tem_menor_precedencia():
    assert expr("x + 1 < y * 2") == BinOp(
        "<", BinOp("+", Var("x"), Num(1)), BinOp("*", Var("y"), Num(2)))


def test_todos_os_operadores_de_comparacao():
    for op in ["<", ">", "<=", ">=", "==", "!="]:
        assert expr(f"a {op} b") == BinOp(op, Var("a"), Var("b"))


def test_booleanos():
    assert expr("true") == Bool(True)
    assert expr("false") == Bool(False)


def test_print():
    assert analisar_texto("print(x + 1);") == Programa(
        [Print(BinOp("+", Var("x"), Num(1)))])


def test_while():
    prog = analisar_texto("while (x < 10) { x = x + 1; }")
    assert prog == Programa([
        While(BinOp("<", Var("x"), Num(10)),
              Bloco([Atribuicao("x", BinOp("+", Var("x"), Num(1)))]))])


def test_for_com_as_tres_clausulas():
    f = analisar_texto("for (i = 0; i < 10; i = i + 1) { print(i); }").comandos[0]
    assert isinstance(f, For)
    assert f.init == Atribuicao("i", Num(0))
    assert f.cond == BinOp("<", Var("i"), Num(10))
    assert f.atualizacao == Atribuicao("i", BinOp("+", Var("i"), Num(1)))
    assert f.corpo == Bloco([Print(Var("i"))])


def test_if_com_e_sem_else():
    prog = analisar_texto("if (x > 0) { print(1); } else { print(0); } if (true) { }")
    assert prog.comandos[0] == If(BinOp(">", Var("x"), Num(0)),
                                  Bloco([Print(Num(1))]), Bloco([Print(Num(0))]))
    assert prog.comandos[1] == If(Bool(True), Bloco([]), None)


def test_blocos_aninhados_e_laco_dentro_de_laco():
    prog = analisar_texto("""
        { x = 1; { y = 2; } }
        while (a > 0) { for (i = 0; i < 2; i = i + 1) { print(i); } a = a - 1; }
    """)
    assert prog.comandos[0] == Bloco([Atribuicao("x", Num(1)),
                                      Bloco([Atribuicao("y", Num(2))])])
    laco = prog.comandos[1]
    assert isinstance(laco, While)
    assert isinstance(laco.corpo.comandos[0], For)


def test_comentarios_sao_ignorados():
    prog = analisar_texto("// comentário\nx = 1; /* bloco */ print(x);")
    assert prog == Programa([Atribuicao("x", Num(1)), Print(Var("x"))])


def test_programa_vazio():
    assert analisar_texto("") == Programa([])


def test_programa_valido_de_exemplo():
    texto = (RAIZ / "exemplos" / "programa_valido.ml").read_text(encoding="utf-8")
    prog = analisar_texto(texto)
    tipos = [type(c).__name__ for c in prog.comandos]
    assert tipos == ["Atribuicao", "While", "Atribuicao", "For", "If"]
