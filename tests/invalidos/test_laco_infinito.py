"""Testes de laço infinito com limite de iterações.
Resultado esperado: o interpretador interrompe o laço ao passar do limite
e levanta LimiteIteracoesError, em vez de travar a suíte de testes."""
import pytest
from src.interpreter import executar_texto, LimiteIteracoesError, LIMITE_ITERACOES


def interrompe(texto, limite=100):
    saida = []
    with pytest.raises(LimiteIteracoesError) as e:
        executar_texto(texto, saida.append, limite_iteracoes=limite)
    return e.value, saida


def test_while_true_e_interrompido():
    e, _ = interrompe("while (true) { }")
    assert e.comando == "while" and e.limite == 100
    assert "laço infinito" in str(e)


def test_while_sem_atualizacao_da_variavel_e_interrompido():
    # Erro clássico: esqueceu de decrementar x.
    e, saida = interrompe("x = 3; while (x > 0) { print(x); }", limite=5)
    assert saida == ["3"] * 5


def test_for_com_atualizacao_na_direcao_errada_e_interrompido():
    e, _ = interrompe("for (i = 0; i < 10; i = i - 1) { }")
    assert e.comando == "for"


def test_laco_no_limite_exato_nao_e_interrompido():
    saida = []
    executar_texto("for (i = 0; i < 5; i = i + 1) { print(i); }",
                   saida.append, limite_iteracoes=5)
    assert len(saida) == 5


def test_limite_padrao_permite_lacos_grandes():
    saida = []
    tabela = executar_texto("s = 0; for (i = 0; i < 1000; i = i + 1) { s = s + 1; }",
                            saida.append)
    assert tabela.buscar("s") == 1000
    assert LIMITE_ITERACOES >= 1000
