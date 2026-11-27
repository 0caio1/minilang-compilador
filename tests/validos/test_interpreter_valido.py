"""Testes do interpretador com programas VÁLIDOS.
Resultado esperado: a saída do `print` e o valor final das variáveis
na tabela de símbolos. Os testes específicos de laço estão em test_lacos.py."""
from pathlib import Path

from src.interpreter import executar_texto, TabelaSimbolos

RAIZ = Path(__file__).resolve().parents[2]


def rodar(texto):
    """Executa o programa e devolve (linhas impressas, variáveis finais)."""
    saida = []
    tabela = executar_texto(texto, saida.append)
    return saida, tabela.como_dict()


def valor(expressao):
    return rodar(f"x = {expressao};")[1]["x"]


# ---------- tabela de símbolos ----------

def test_tabela_insere_e_busca():
    t = TabelaSimbolos()
    t.inserir("x", 10)
    assert t.buscar("x") == 10
    assert t.contem("x") and not t.contem("y")


def test_tabela_inserir_de_novo_atualiza_o_valor():
    t = TabelaSimbolos()
    t.inserir("x", 1)
    t.inserir("x", 2)
    assert t.buscar("x") == 2


# ---------- expressões ----------

def test_aritmetica_respeita_precedencia():
    assert valor("1 + 2 * 3") == 7
    assert valor("(1 + 2) * 3") == 9


def test_subtracao_associativa_a_esquerda():
    assert valor("10 - 3 - 2") == 5


def test_divisao_inteira():
    assert valor("7 / 2") == 3
    assert valor("8 / 4 / 2") == 1


def test_divisao_negativa_trunca_em_direcao_a_zero():
    assert valor("(0 - 7) / 2") == -3
    assert valor("7 / (0 - 2)") == -3


def test_negativo_com_zero_menos():
    assert valor("0 - 1") == -1


def test_comparacoes_resultam_em_booleano():
    assert valor("3 < 5") is True
    assert valor("3 > 5") is False
    assert valor("5 <= 5") is True
    assert valor("4 >= 5") is False
    assert valor("2 == 2") is True
    assert valor("2 != 2") is False


def test_igualdade_entre_booleanos():
    assert valor("true == true") is True
    assert valor("true != false") is True


# ---------- comandos ----------

def test_print_de_inteiro_e_booleano():
    saida, _ = rodar("print(42); print(true); print(1 > 2);")
    assert saida == ["42", "true", "false"]


def test_atribuicao_e_reatribuicao():
    _, amb = rodar("a = 1; a = a + 1;")
    assert amb["a"] == 2


def test_if_executa_o_entao():
    saida, _ = rodar("if (1 < 2) { print(1); } else { print(2); }")
    assert saida == ["1"]


def test_if_executa_o_senao():
    saida, _ = rodar("if (1 > 2) { print(1); } else { print(2); }")
    assert saida == ["2"]


def test_if_sem_else_com_condicao_falsa_nao_faz_nada():
    saida, _ = rodar("if (false) { print(1); }")
    assert saida == []


def test_bloco_nao_cria_escopo():
    _, amb = rodar("{ y = 5; } z = y + 1;")
    assert amb["z"] == 6


def test_programa_vazio():
    saida, amb = rodar("")
    assert saida == [] and amb == {}


def test_exemplo_do_enunciado():
    saida, amb = rodar(
        "x = 10; y = 2 * (x + 5);"
        "while (x > 0) { print(x); x = x - 1; }"
        "soma = 0; for (i = 0; i < 5; i = i + 1) { soma = soma + i; }"
        "if (soma > 20) { print(soma); } else { print(0); }")
    assert saida == [str(n) for n in range(10, 0, -1)] + ["0"]
    assert amb["y"] == 30 and amb["soma"] == 10


def test_programa_valido_do_repositorio():
    texto = (RAIZ / "exemplos" / "programa_valido.ml").read_text(encoding="utf-8")
    saida, amb = rodar(texto)
    assert saida == ["3", "2", "1", "10"]
    assert amb["soma"] == 10
