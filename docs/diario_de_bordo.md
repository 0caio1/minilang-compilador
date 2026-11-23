# Diário de bordo

## Semana 1

### 23/11/2026
- **Feito:** criamos o repositório e recebemos os rascunhos da gramática, do lexer, da AST, dos testes e dos exemplos, gerados pelo Claude.
- **Uso de IA:** o Claude gerou esses rascunhos. O grupo usou esse material como base, revisou e adaptou.
- **Feito:** rodamos os testes (21 passando) e commitamos por partes: estrutura, gramática, lexer, testes do lexer, AST com testes e programas de exemplo.
- **Problema identificado:** ao revisar o código, notamos que o lexer usa `isalpha()` e `isdigit()`, que aceitam letras acentuadas e outros dígitos, enquanto a gramática só prevê ASCII. Vamos corrigir em um commit separado, com teste novo.
- **Próximos passos:** correção do lexer, tabela de transições do AFD, 5 exemplos comentados, parser e interpretador.
