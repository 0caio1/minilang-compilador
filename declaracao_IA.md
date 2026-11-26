# Declaração de uso de IA generativa

**Integrantes:** Caio Leal, Hapolo Luiz, Salatiel Batista

**Houve uso de IA generativa neste projeto:** Sim.

**Ferramenta e modelo:** Claude (Sonnet 5.5), da Anthropic.
 
## Como a IA foi usada
 
A IA serviu como ponto de partida. Ela gerou rascunhos iniciais, e o grupo usou esse material como base para desenvolver o projeto: leu o código, testou, adaptou o que precisava e passou a responder por ele. Nenhum arquivo foi entregue sem ser revisado e entendido pelo grupo.
 
| Etapa | Finalidade do uso da IA | Responsável |
|---|---|---|
| Gramática (item a) | Rascunho inicial da EBNF e da tabela de precedência | Caio |
| Programas de exemplo (item a) | Rascunho de `programa_valido.ml` e `programa_invalido.ml` | Caio |
| Lexer (item b) | Rascunho de `src/lexer.py` e dos testes do lexer | Caio |
| AST (item d) | Rascunho de `src/ast_nodes.py` e dos testes da AST | Caio |
| Tabela de transições do AFD (item b) | Rascunho da tabela derivada do `lexer.py`, com checagem por simulação | Caio |
 
## O que o grupo fez em cima do rascunho
 
- Rodamos a suíte de testes (21 testes passando) antes de commitar o lexer.
- Conferimos arquivo por arquivo o conteúdo dos testes, dos exemplos e da AST antes de cada commit.
- Caio aplicou no lexer a correção apontada pelo Claude (identificadores e números só em ASCII) e incluiu os testes novos que cobrem o caso.
- Caio conferiu a tabela de transições do AFD seguindo-a à mão com diferentes entradas.

## Observações
 
- Os detalhes de cada uso, o que foi aceito, reescrito ou descartado e os erros da IA que precisaram de correção estão em `docs/diario_de_bordo.md` e no `docs/relatorio.pdf`.
- Todos os integrantes conseguem explicar e defender o código entregue na arguição.
- Esta tabela é atualizada sempre que a IA for usada em uma etapa nova.
