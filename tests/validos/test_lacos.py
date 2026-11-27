"""Testes de laços (while e for) com programas VÁLIDOS.
Casos de borda pedidos no item (g): laço que não executa, que executa
1 vez, que executa N vezes, e for cuja atualização altera a variável
de controle. Resultado esperado: a saída do `print` e as variáveis finais."""
from src.interpreter import executar_texto


def rodar(texto):
    saida = []
    tabela = executar_texto(texto, saida.append)
    return saida, tabela.como_dict()


# ---------- while ----------

def test_while_nao_executa_com_condicao_falsa_na_entrada():
    saida, amb = rodar("x = 0; while (x > 0) { print(x); x = x - 1; }")
    assert saida == []
    assert amb["x"] == 0


def test_while_executa_uma_vez():
    saida, amb = rodar("x = 1; while (x > 0) { print(x); x = x - 1; }")
    assert saida == ["1"]
    assert amb["x"] == 0


def test_while_executa_n_vezes():
    saida, amb = rodar("x = 5; while (x > 0) { print(x); x = x - 1; }")
    assert saida == ["5", "4", "3", "2", "1"]
    assert amb["x"] == 0


def test_while_com_false_literal_nao_executa():
    saida, _ = rodar("while (false) { print(1); }")
    assert saida == []


# ---------- for ----------

def test_for_nao_executa_com_condicao_falsa_na_entrada():
    saida, amb = rodar("for (i = 5; i < 5; i = i + 1) { print(i); }")
    assert saida == []
    # A inicialização roda mesmo quando o corpo não roda.
    assert amb["i"] == 5


def test_for_executa_uma_vez():
    saida, amb = rodar("for (i = 0; i < 1; i = i + 1) { print(i); }")
    assert saida == ["0"]
    assert amb["i"] == 1


def test_for_executa_n_vezes():
    saida, amb = rodar("soma = 0; for (i = 0; i < 5; i = i + 1) { soma = soma + i; }")
    assert amb["soma"] == 10
    assert amb["i"] == 5


def test_for_atualizacao_altera_a_variavel_de_controle():
    # Passo 2: a atualização muda i a cada volta, e é ela que encerra o laço.
    saida, amb = rodar("for (i = 0; i < 10; i = i + 2) { print(i); }")
    assert saida == ["0", "2", "4", "6", "8"]
    assert amb["i"] == 10


def test_for_decrescente():
    saida, _ = rodar("for (i = 3; i > 0; i = i - 1) { print(i); }")
    assert saida == ["3", "2", "1"]


def test_for_ordem_inicializacao_condicao_corpo_atualizacao():
    # O corpo vê o valor de i ANTES da atualização da mesma volta.
    saida, _ = rodar("for (i = 0; i < 2; i = i + 1) { print(i); }")
    assert saida == ["0", "1"]


def test_variavel_do_for_continua_existindo_depois_do_laco():
    _, amb = rodar("for (i = 0; i < 3; i = i + 1) { }")
    assert amb["i"] == 3


def test_lacos_aninhados():
    saida, _ = rodar(
        "for (i = 1; i <= 2; i = i + 1) {"
        "  for (j = 1; j <= 2; j = j + 1) { print(i * 10 + j); }"
        "}")
    assert saida == ["11", "12", "21", "22"]


def test_while_dentro_de_for():
    saida, _ = rodar(
        "for (i = 1; i <= 2; i = i + 1) {"
        "  j = i; while (j > 0) { print(j); j = j - 1; }"
        "}")
    assert saida == ["1", "2", "1"]
