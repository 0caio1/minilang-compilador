"""Parser descendente recursivo da MiniLang.

Cada regra da EBNF em docs/gramatica.md vira um método com o mesmo nome.
A precedência sai da própria hierarquia das regras
(comparacao -> soma -> termo -> fator) e a associatividade à esquerda
sai dos laços em `soma` e `termo`.
"""
from src.lexer import tokenizar
from src.ast_nodes import (Num, Bool, Var, BinOp, Atribuicao, Print, Bloco,
                           If, While, For, Programa)

OPS_COMPARACAO = {"LT": "<", "GT": ">", "LE": "<=", "GE": ">=", "EQ": "==", "NE": "!="}
OPS_SOMA = {"MAIS": "+", "MENOS": "-"}
OPS_TERMO = {"VEZES": "*", "DIV": "/"}

DESCRICAO = {
    "SEMI": "';'", "LPAREN": "'('", "RPAREN": "')'", "LBRACE": "'{'", "RBRACE": "'}'",
    "ATRIB": "'='", "ID": "identificador", "EOF": "fim do arquivo",
}


class ParseError(Exception):
    """Erro sintático, com posição (linha, coluna) do token problemático."""

    def __init__(self, mensagem, linha, coluna):
        super().__init__(f"Erro sintático na linha {linha}, coluna {coluna}: {mensagem}")
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna


def _descrever(token):
    if token.tipo == "EOF":
        return "fim do arquivo"
    return f"'{token.valor}'"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    @property
    def atual(self):
        return self.tokens[self.pos]

    def avancar(self):
        token = self.atual
        if token.tipo != "EOF":
            self.pos += 1
        return token

    def erro(self, mensagem, token=None):
        token = token or self.atual
        raise ParseError(mensagem, token.linha, token.coluna)

    def consumir(self, tipo, contexto=""):
        if self.atual.tipo != tipo:
            esperado = DESCRICAO.get(tipo, tipo)
            sufixo = f" {contexto}" if contexto else ""
            self.erro(f"esperado {esperado}{sufixo}, encontrado {_descrever(self.atual)}")
        return self.avancar()

    # programa = { comando } ;
    def programa(self):
        comandos = []
        while self.atual.tipo != "EOF":
            comandos.append(self.comando())
        return Programa(comandos)

    # comando = atribuicao ";" | impressao | condicional | enquanto | para | bloco ;
    def comando(self):
        tipo = self.atual.tipo
        if tipo == "ID":
            atrib = self.atribuicao()
            self.consumir("SEMI", "após a atribuição")
            return atrib
        if tipo == "PRINT":
            return self.impressao()
        if tipo == "IF":
            return self.condicional()
        if tipo == "WHILE":
            return self.enquanto()
        if tipo == "FOR":
            return self.para()
        if tipo == "LBRACE":
            return self.bloco()
        if tipo == "ELSE":
            self.erro("'else' sem 'if' correspondente")
        self.erro(f"início de comando inválido: {_descrever(self.atual)}")

    # bloco = "{" { comando } "}" ;
    def bloco(self):
        abre = self.consumir("LBRACE", "para abrir o bloco")
        comandos = []
        while self.atual.tipo not in ("RBRACE", "EOF"):
            comandos.append(self.comando())
        if self.atual.tipo == "EOF":
            self.erro(f"bloco aberto na linha {abre.linha} não foi fechado com '}}'")
        self.avancar()
        return Bloco(comandos)

    # impressao = "print" "(" expressao ")" ";" ;
    def impressao(self):
        self.avancar()
        self.consumir("LPAREN", "após 'print'")
        expr = self.expressao()
        self.consumir("RPAREN", "para fechar o 'print'")
        self.consumir("SEMI", "após o 'print'")
        return Print(expr)

    # condicional = "if" "(" expressao ")" bloco [ "else" bloco ] ;
    def condicional(self):
        self.avancar()
        self.consumir("LPAREN", "após 'if'")
        cond = self.expressao()
        self.consumir("RPAREN", "para fechar a condição do 'if'")
        entao = self.bloco()
        senao = None
        if self.atual.tipo == "ELSE":
            self.avancar()
            senao = self.bloco()
        return If(cond, entao, senao)

    # enquanto = "while" "(" expressao ")" bloco ;
    def enquanto(self):
        self.avancar()
        self.consumir("LPAREN", "após 'while'")
        cond = self.expressao()
        self.consumir("RPAREN", "para fechar a condição do 'while'")
        return While(cond, self.bloco())

    # para = "for" "(" atribuicao ";" expressao ";" atribuicao ")" bloco ;
    def para(self):
        self.avancar()
        self.consumir("LPAREN", "após 'for'")
        if self.atual.tipo != "ID":
            self.erro("a inicialização do 'for' deve ser uma atribuição")
        init = self.atribuicao()
        self.consumir("SEMI", "após a inicialização do 'for'")
        if self.atual.tipo == "SEMI":
            self.erro("a condição do 'for' é obrigatória")
        cond = self.expressao()
        self.consumir("SEMI", "após a condição do 'for' (falta a cláusula de atualização?)")
        if self.atual.tipo != "ID":
            self.erro("a atualização do 'for' deve ser uma atribuição")
        atualizacao = self.atribuicao()
        self.consumir("RPAREN", "para fechar o cabeçalho do 'for'")
        return For(init, cond, atualizacao, self.bloco())

    # atribuicao = ID "=" expressao ;
    def atribuicao(self):
        nome = self.consumir("ID").valor
        self.consumir("ATRIB", f"após '{nome}'")
        return Atribuicao(nome, self.expressao())

    # expressao = comparacao ;
    def expressao(self):
        return self.comparacao()

    # comparacao = soma [ op_rel soma ] ;
    def comparacao(self):
        esq = self.soma()
        if self.atual.tipo in OPS_COMPARACAO:
            op = OPS_COMPARACAO[self.avancar().tipo]
            esq = BinOp(op, esq, self.soma())
            if self.atual.tipo in OPS_COMPARACAO:
                self.erro("operadores de comparação não são associativos "
                          "(ex.: 'a < b < c' não é permitido)")
        return esq

    # soma = termo { ( "+" | "-" ) termo } ;
    def soma(self):
        esq = self.termo()
        while self.atual.tipo in OPS_SOMA:
            op = OPS_SOMA[self.avancar().tipo]
            esq = BinOp(op, esq, self.termo())
        return esq

    # termo = fator { ( "*" | "/" ) fator } ;
    def termo(self):
        esq = self.fator()
        while self.atual.tipo in OPS_TERMO:
            op = OPS_TERMO[self.avancar().tipo]
            esq = BinOp(op, esq, self.fator())
        return esq

    # fator = NUM | "true" | "false" | ID | "(" expressao ")" ;
    def fator(self):
        token = self.atual
        if token.tipo == "NUM":
            self.avancar()
            return Num(int(token.valor))
        if token.tipo == "TRUE":
            self.avancar()
            return Bool(True)
        if token.tipo == "FALSE":
            self.avancar()
            return Bool(False)
        if token.tipo == "ID":
            self.avancar()
            return Var(token.valor)
        if token.tipo == "LPAREN":
            self.avancar()
            expr = self.expressao()
            self.consumir("RPAREN", "para fechar a expressão")
            return expr
        self.erro(f"esperada uma expressão, encontrado {_descrever(token)}")


def analisar(tokens):
    """Recebe a lista de tokens do lexer e devolve a AST (Programa)."""
    return Parser(tokens).programa()


def analisar_texto(texto):
    """Atalho: tokeniza e analisa o código-fonte de uma vez."""
    return analisar(tokenizar(texto))
