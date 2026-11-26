"""Testes do lexer com entradas VÁLIDAS.
Resultado esperado: a lista de tipos de token indicada em cada teste."""
from src.lexer import tokenizar


def tipos(texto):
    return [t.tipo for t in tokenizar(texto)]


def test_atribuicao_simples():
    assert tipos("x = 10;") == ["ID", "ATRIB", "NUM", "SEMI", "EOF"]


def test_palavras_reservadas():
    assert tipos("while for if else print true false") == [
        "WHILE", "FOR", "IF", "ELSE", "PRINT", "TRUE", "FALSE", "EOF"]


def test_identificador_parecido_com_reservada():
    # 'whilex' e 'format' NÃO são reservadas (casamento pelo lexema inteiro)
    assert tipos("whilex format") == ["ID", "ID", "EOF"]


def test_operadores_de_dois_caracteres():
    assert tipos("<= >= == !=") == ["LE", "GE", "EQ", "NE", "EOF"]


def test_operadores_de_um_caractere():
    assert tipos("< > = + - * /") == [
        "LT", "GT", "ATRIB", "MAIS", "MENOS", "VEZES", "DIV", "EOF"]


def test_comentario_de_linha_e_ignorado():
    assert tipos("x = 1; // isto é ignorado\ny = 2;") == [
        "ID", "ATRIB", "NUM", "SEMI", "ID", "ATRIB", "NUM", "SEMI", "EOF"]


def test_comentario_de_bloco_e_ignorado():
    assert tipos("x /* nada */ = 1;") == ["ID", "ATRIB", "NUM", "SEMI", "EOF"]


def test_posicao_do_token():
    toks = tokenizar("x = 1;\ny = 2;")
    y = [t for t in toks if t.valor == "y"][0]
    assert (y.linha, y.coluna) == (2, 1)


def test_for_completo():
    assert tipos("for (i = 0; i < 10; i = i + 1) { print(i); }") == [
        "FOR", "LPAREN", "ID", "ATRIB", "NUM", "SEMI",
        "ID", "LT", "NUM", "SEMI",
        "ID", "ATRIB", "ID", "MAIS", "NUM", "RPAREN",
        "LBRACE", "PRINT", "LPAREN", "ID", "RPAREN", "SEMI", "RBRACE", "EOF"]


def test_entrada_vazia():
    assert tipos("") == ["EOF"]

def test_identificadores_ascii_com_underscore_e_digito():
    assert tipos("_a1 B_2 x9") == ["ID", "ID", "ID", "EOF"]
