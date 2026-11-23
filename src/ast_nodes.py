"""Nós da AST da MiniLang.

Parênteses, ';' e chaves não aparecem aqui: a estrutura da árvore já
carrega a informação que eles expressavam na árvore concreta.
"""
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class Num:
    valor: int


@dataclass
class Bool:
    valor: bool


@dataclass
class Var:
    nome: str


@dataclass
class BinOp:
    op: str  # + - * / < > <= >= == !=
    esq: "Expr"
    dir: "Expr"


Expr = Union[Num, Bool, Var, BinOp]


@dataclass
class Atribuicao:
    nome: str
    expr: Expr


@dataclass
class Print:
    expr: Expr


@dataclass
class Bloco:
    comandos: List["Comando"]


@dataclass
class If:
    cond: Expr
    entao: Bloco
    senao: Optional[Bloco] = None


@dataclass
class While:
    cond: Expr
    corpo: Bloco


@dataclass
class For:
    init: Atribuicao
    cond: Expr
    atualizacao: Atribuicao
    corpo: Bloco


Comando = Union[Atribuicao, Print, Bloco, If, While, For]


@dataclass
class Programa:
    comandos: List[Comando]
