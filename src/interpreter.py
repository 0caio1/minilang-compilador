"""Interpretador da MiniLang e tabela de símbolos.

Percorre a AST gerada pelo parser (src/parser.py) e executa cada nó.
Um método `executar_<Nó>` para cada comando e um `avaliar_<Nó>` para cada
expressão: o despacho é feito pelo nome da classe do nó.

Decisões semânticas (registradas também em docs/gramatica.md):
- Há dois tipos de valor: inteiro e booleano.
- Uma única tabela de símbolos global. Escopo aninhado está fora do escopo
  do projeto, então bloco não cria escopo e a variável de controle do `for`
  continua existindo depois do laço.
- Usar uma variável antes de atribuí-la é erro.
- `+ - * /` e `< > <= >=` só aceitam inteiros.
- `==` e `!=` só comparam valores do mesmo tipo.
- `/` é divisão inteira truncada em direção a zero (como em C e Java):
  (0 - 7) / 2 dá -3. Dividir por zero é erro.
- A condição de `if`, `while` e `for` precisa ser booleana.
- Cada laço pode repetir no máximo `limite_iteracoes` vezes; passar disso
  interrompe a execução, para um laço infinito não travar o programa.
- `print` mostra booleanos como `true` / `false`, na grafia da MiniLang.

Uso pela linha de comando:
    python -m src.interpreter exemplos/programa_valido.ml
"""
import sys

from src.lexer import LexError
from src.parser import ParseError, analisar_texto

LIMITE_ITERACOES = 10_000


class SemanticError(Exception):
    """Erro semântico detectado na execução (tipo, variável, divisão por zero)."""

    def __init__(self, mensagem):
        super().__init__(f"Erro semântico: {mensagem}")
        self.mensagem = mensagem


class LimiteIteracoesError(Exception):
    """Um laço passou do limite de iterações (provável laço infinito)."""

    def __init__(self, comando, limite):
        super().__init__(
            f"Erro de execução: o '{comando}' passou de {limite} iterações "
            f"(provável laço infinito)")
        self.comando = comando
        self.limite = limite


class TabelaSimbolos:
    """Tabela de símbolos: associa o nome de cada variável ao seu valor atual.

    Estrutura: um dicionário (tabela hash), com inserção e busca em O(1)
    no caso médio. Como a MiniLang não tem funções nem escopo aninhado,
    uma única tabela global basta.
    """

    def __init__(self):
        self._simbolos = {}

    def inserir(self, nome, valor):
        """Cria a variável ou atualiza o valor dela (atribuição)."""
        self._simbolos[nome] = valor

    def buscar(self, nome):
        """Devolve o valor da variável; erro se ela nunca foi atribuída."""
        if nome not in self._simbolos:
            raise SemanticError(f"variável '{nome}' usada antes de ser definida")
        return self._simbolos[nome]

    def contem(self, nome):
        return nome in self._simbolos

    def como_dict(self):
        """Cópia do conteúdo, para inspeção nos testes."""
        return dict(self._simbolos)


OPS_ARITMETICOS = {"+", "-", "*", "/"}
OPS_ORDEM = {"<", ">", "<=", ">="}
OPS_IGUALDADE = {"==", "!="}


def _eh_int(valor):
    # Em Python, bool é subclasse de int (isinstance(True, int) é True).
    # Por isso o booleano precisa ser excluído explicitamente.
    return isinstance(valor, int) and not isinstance(valor, bool)


def _eh_bool(valor):
    return isinstance(valor, bool)


def _nome_tipo(valor):
    return "booleano" if _eh_bool(valor) else "inteiro"


def formatar(valor):
    """Converte um valor da MiniLang para texto, como o `print` mostra."""
    if _eh_bool(valor):
        return "true" if valor else "false"
    return str(valor)


def _dividir(a, b):
    if b == 0:
        raise SemanticError("divisão por zero")
    quociente = abs(a) // abs(b)
    return quociente if (a >= 0) == (b >= 0) else -quociente


class Interpretador:
    def __init__(self, saida=print, limite_iteracoes=LIMITE_ITERACOES):
        # `saida` recebe cada linha impressa. Nos testes, passamos
        # uma lista.append para capturar o que foi impresso.
        self.tabela = TabelaSimbolos()
        self.saida = saida
        self.limite_iteracoes = limite_iteracoes

    # ---------- comandos ----------

    def executar(self, no):
        metodo = getattr(self, f"executar_{type(no).__name__}")
        metodo(no)

    def executar_Programa(self, no):
        for comando in no.comandos:
            self.executar(comando)

    def executar_Bloco(self, no):
        for comando in no.comandos:
            self.executar(comando)

    def executar_Atribuicao(self, no):
        self.tabela.inserir(no.nome, self.avaliar(no.expr))

    def executar_Print(self, no):
        self.saida(formatar(self.avaliar(no.expr)))

    def executar_If(self, no):
        if self.condicao(no.cond, "if"):
            self.executar(no.entao)
        elif no.senao is not None:
            self.executar(no.senao)

    def executar_While(self, no):
        iteracoes = 0
        while self.condicao(no.cond, "while"):
            iteracoes = self.contar_iteracao(iteracoes, "while")
            self.executar(no.corpo)

    def executar_For(self, no):
        self.executar(no.init)
        iteracoes = 0
        while self.condicao(no.cond, "for"):
            iteracoes = self.contar_iteracao(iteracoes, "for")
            self.executar(no.corpo)
            self.executar(no.atualizacao)

    def contar_iteracao(self, iteracoes, comando):
        iteracoes += 1
        if iteracoes > self.limite_iteracoes:
            raise LimiteIteracoesError(comando, self.limite_iteracoes)
        return iteracoes

    def condicao(self, expr, comando):
        valor = self.avaliar(expr)
        if not _eh_bool(valor):
            raise SemanticError(
                f"a condição do '{comando}' deve ser booleana, "
                f"mas resultou em {_nome_tipo(valor)} ({formatar(valor)})")
        return valor

    # ---------- expressões ----------

    def avaliar(self, no):
        metodo = getattr(self, f"avaliar_{type(no).__name__}")
        return metodo(no)

    def avaliar_Num(self, no):
        return no.valor

    def avaliar_Bool(self, no):
        return no.valor

    def avaliar_Var(self, no):
        return self.tabela.buscar(no.nome)

    def avaliar_BinOp(self, no):
        esq = self.avaliar(no.esq)
        dir = self.avaliar(no.dir)
        op = no.op

        if op in OPS_ARITMETICOS or op in OPS_ORDEM:
            if not (_eh_int(esq) and _eh_int(dir)):
                raise SemanticError(
                    f"o operador '{op}' exige inteiros, recebeu "
                    f"{_nome_tipo(esq)} e {_nome_tipo(dir)}")
            if op == "+":
                return esq + dir
            if op == "-":
                return esq - dir
            if op == "*":
                return esq * dir
            if op == "/":
                return _dividir(esq, dir)
            if op == "<":
                return esq < dir
            if op == ">":
                return esq > dir
            if op == "<=":
                return esq <= dir
            return esq >= dir

        if op in OPS_IGUALDADE:
            if _eh_bool(esq) != _eh_bool(dir):
                raise SemanticError(
                    f"o operador '{op}' não compara {_nome_tipo(esq)} "
                    f"com {_nome_tipo(dir)}")
            return esq == dir if op == "==" else esq != dir

        raise SemanticError(f"operador desconhecido '{op}'")


def executar(programa, saida=print, limite_iteracoes=LIMITE_ITERACOES):
    """Executa uma AST (Programa) e devolve a tabela de símbolos final."""
    interpretador = Interpretador(saida, limite_iteracoes)
    interpretador.executar(programa)
    return interpretador.tabela


def executar_texto(texto, saida=print, limite_iteracoes=LIMITE_ITERACOES):
    """Atalho: tokeniza, analisa e executa o código-fonte de uma vez."""
    return executar(analisar_texto(texto), saida, limite_iteracoes)


def main(argv):
    if len(argv) != 2:
        print("uso: python -m src.interpreter <arquivo.ml>", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as arquivo:
            texto = arquivo.read()
    except OSError as e:
        print(f"não foi possível abrir '{argv[1]}': {e.strerror}", file=sys.stderr)
        return 2
    try:
        executar_texto(texto)
    except (LexError, ParseError, SemanticError, LimiteIteracoesError) as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
