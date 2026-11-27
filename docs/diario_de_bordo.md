# Diário de bordo

## Semana 1

### 23/11/2026
- **Feito:** criamos o repositório e recebemos os rascunhos da gramática, do lexer, da AST, dos testes e dos exemplos, gerados pelo Claude.
- **Uso de IA:** o Claude gerou esses rascunhos. O grupo usou esse material como base, revisou e adaptou.
- **Feito:** rodamos os testes (21 passando) e commitamos por partes: estrutura, gramática, lexer, testes do lexer, AST com testes e programas de exemplo.
- **Problema identificado:** ao revisar o código, notamos que o lexer usa `isalpha()` e `isdigit()`, que aceitam letras acentuadas e outros dígitos, enquanto a gramática só prevê ASCII. Vamos corrigir em um commit separado, com teste novo.
- **Próximos passos:** correção do lexer, tabela de transições do AFD, 5 exemplos comentados, parser e interpretador.


### 26/11/2026
- **Correção feita:** aplicamos no `lexer.py` a correção identificada pelo Claude (listas explícitas de letras e dígitos ASCII no lugar de `isalpha()`, `isdigit()` e `isalnum()`) e acrescentamos 3 testes (`ação`, `5²` e identificadores ASCII). A suíte passou de 21 para 24 testes. Conceito: o lexer estava reconhecendo uma linguagem maior do que a definida pelas expressões regulares da gramática.
- **Tabela do AFD:** o Claude montou um rascunho da tabela de transições a partir do `lexer.py`, com uma checagem por simulação (200 mil entradas aleatórias, sem divergência com o lexer). Eu conferi a tabela seguindo-a à mão com diferentes entradas.
- **Exemplos comentados:** o Claude sugeriu os 5 programas. Eu escrevi as justificativas dos exemplos e o Claude revisou e sugeriu ajustes.
- **Parser (Hapolo):** o Claude (Opus 5.5) gerou o rascunho de `src/parser.py`, um parser descendente recursivo com um método por regra da EBNF, e os testes `test_parser_valido.py` e `test_parser_invalido.py`. A suíte passou de 24 para 53 testes.
- **Decisão:** o menos unário (`-1`) continua fora da linguagem, porque a EBNF só define `-` como operador binário. Valores negativos são obtidos com `0 - 1`.

### 27/11/2026
- **Interpretador (Salatiel):** o Claude (Opus 5.5) gerou o rascunho de `src/interpreter.py` (interpretador que percorre a AST, com um método por tipo de nó, e a classe `TabelaSimbolos` com `inserir` e `buscar`) e dos testes `test_interpreter_valido.py`, `test_interpreter_invalido.py`, `test_lacos.py` e `test_laco_infinito.py`.
- **Erro da IA corrigido:** o primeiro rascunho usou nomes de arquivo em português (`interpretador.py`), um dicionário solto no lugar de uma tabela de símbolos e não tinha limite de iterações. Ao comparar com o enunciado, renomeamos os arquivos, criamos a classe `TabelaSimbolos` e acrescentamos o limite de 10.000 iterações por laço, com os testes de laço infinito.
- **Decisões semânticas:** divisão inteira truncada em direção a zero; operadores aritméticos e de ordem só com inteiros; `==` e `!=` só entre valores do mesmo tipo; uma única tabela de símbolos global. As regras foram registradas em `docs/gramatica.md`.
- **Problema identificado:** em Python, `bool` é subclasse de `int`, então `true + 1` daria `2` e `1 == true` daria `True` sem erro. O interpretador testa o tipo booleano antes do inteiro, e há testes cobrindo os dois casos.
- **Limitação:** os nós da AST não guardam linha e coluna, então os erros semânticos saem sem posição, ao contrário dos erros léxicos e sintáticos.
