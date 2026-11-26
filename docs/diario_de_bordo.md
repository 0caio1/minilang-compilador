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