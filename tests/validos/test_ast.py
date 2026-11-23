"""Testes que constroem e verificam a AST"""
from src.ast_nodes import (Num, Bool, Var, BinOp, Atribuicao, Print, Bloco,
                           If, While, For, Programa)


def test_ast_de_1_mais_2_vezes_3():
    # 1 + 2 * 3  ->  +(1, *(2, 3))
    ast = BinOp("+", Num(1), BinOp("*", Num(2), Num(3)))
    assert ast.op == "+"
    assert ast.esq == Num(1)
    assert ast.dir == BinOp("*", Num(2), Num(3))


def test_ast_de_parenteses_muda_a_arvore():
    # (1 + 2) * 3  ->  *(+(1, 2), 3)   (parênteses não viram nó)
    ast = BinOp("*", BinOp("+", Num(1), Num(2)), Num(3))
    assert ast.op == "*"
    assert ast.esq == BinOp("+", Num(1), Num(2))


def test_ast_do_while():
    w = While(BinOp(">", Var("x"), Num(0)),
              Bloco([Print(Var("x")),
                     Atribuicao("x", BinOp("-", Var("x"), Num(1)))]))
    assert isinstance(w.cond, BinOp)
    assert len(w.corpo.comandos) == 2


def test_ast_do_for_com_as_tres_clausulas():
    f = For(Atribuicao("i", Num(0)),
            BinOp("<", Var("i"), Num(10)),
            Atribuicao("i", BinOp("+", Var("i"), Num(1))),
            Bloco([Print(Var("i"))]))
    assert f.init == Atribuicao("i", Num(0))
    assert f.cond.op == "<"
    assert f.atualizacao.nome == "i"
    assert len(f.corpo.comandos) == 1


def test_if_sem_else():
    assert If(Bool(True), Bloco([])).senao is None


def test_programa_completo():
    p = Programa([Atribuicao("x", Num(1)), Print(Var("x"))])
    assert len(p.comandos) == 2
