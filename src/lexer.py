"""Lexer da MiniLang.

Implementado como um autômato finito determinístico escrito à mão:
cada ramo do `if` em `tokenizar` corresponde a um grupo de estados do AFD.
"""
from dataclasses import dataclass

PALAVRAS_RESERVADAS = {
    "if": "IF", "else": "ELSE", "while": "WHILE", "for": "FOR",
    "print": "PRINT", "true": "TRUE", "false": "FALSE",
}

DIGITOS = "0123456789"
LETRAS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
INICIO_ID = LETRAS + "_"
CORPO_ID = LETRAS + DIGITOS + "_"

SIMBOLOS = {
    "(": "LPAREN", ")": "RPAREN", "{": "LBRACE", "}": "RBRACE", ";": "SEMI",
    "+": "MAIS", "-": "MENOS", "*": "VEZES", "/": "DIV",
}


class LexError(Exception):
    """Erro léxico, com posição (linha, coluna) do problema."""

    def __init__(self, mensagem, linha, coluna):
        super().__init__(f"Erro léxico na linha {linha}, coluna {coluna}: {mensagem}")
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna


@dataclass(frozen=True)
class Token:
    tipo: str
    valor: str
    linha: int
    coluna: int


def tokenizar(texto):
    """Converte o texto-fonte em uma lista de tokens terminada por EOF."""
    tokens = []
    i, linha, coluna = 0, 1, 1
    n = len(texto)

    def avancar(qtd=1):
        nonlocal i, linha, coluna
        for _ in range(qtd):
            if texto[i] == "\n":
                linha += 1
                coluna = 1
            else:
                coluna += 1
            i += 1

    while i < n:
        c = texto[i]

        # espaços em branco
        if c in " \t\r\n":
            avancar()
            continue

        # comentários: // até o fim da linha, /* ... */ em bloco
        if c == "/" and i + 1 < n and texto[i + 1] == "/":
            while i < n and texto[i] != "\n":
                avancar()
            continue
        if c == "/" and i + 1 < n and texto[i + 1] == "*":
            l0, c0 = linha, coluna
            avancar(2)
            while i < n and not (texto[i] == "*" and i + 1 < n and texto[i + 1] == "/"):
                avancar()
            if i >= n:
                raise LexError("comentário não fechado", l0, c0)
            avancar(2)
            continue

        l0, c0 = linha, coluna

        # número: digito+ (não pode vir colado em letra, ex.: 1x)
        if c in DIGITOS:
            ini = i
            while i < n and texto[i] in DIGITOS:
                avancar()
            if i < n and texto[i] in INICIO_ID:
                raise LexError(
                    "identificador não pode começar com dígito "
                    f"('{texto[ini:i + 1]}...')", l0, c0)
            tokens.append(Token("NUM", texto[ini:i], l0, c0))
            continue

        # identificador ou palavra reservada
        if c in INICIO_ID:
            ini = i
            while i < n and texto[i] in CORPO_ID:
                avancar()
            lex = texto[ini:i]
            tokens.append(Token(PALAVRAS_RESERVADAS.get(lex, "ID"), lex, l0, c0))
            continue

        # operadores de 1 ou 2 caracteres
        if c in "<>=!":
            if i + 1 < n and texto[i + 1] == "=":
                lex = c + "="
                avancar(2)
                nome = {"<=": "LE", ">=": "GE", "==": "EQ", "!=": "NE"}[lex]
                tokens.append(Token(nome, lex, l0, c0))
            elif c == "!":
                raise LexError("'!' sozinho não é válido (use '!=')", l0, c0)
            else:
                avancar()
                nome = {"<": "LT", ">": "GT", "=": "ATRIB"}[c]
                tokens.append(Token(nome, c, l0, c0))
            continue

        # símbolos simples
        if c in SIMBOLOS:
            avancar()
            tokens.append(Token(SIMBOLOS[c], c, l0, c0))
            continue

        raise LexError(f"caractere inválido '{c}'", l0, c0)

    tokens.append(Token("EOF", "", linha, coluna))
    return tokens
