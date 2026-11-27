# MiniLang — compilador-intérprete

Projeto da II Unidade de Linguagens Formais e Compiladores (UNIT, Ciência da Computação).

**Integrantes:** Caio Leal, Hapolo Luiz, Salatiel Batista

**Ferramenta de IA utilizada:** Claude (Sonnet 5.5), da Anthropic, como copiloto de desenvolvimento.
Detalhes em `declaracao_IA.md` e `docs/diario_de_bordo.md`.

## Requisitos
- Python 3.10+
- `pip install -r requirements.txt`

## Executar os testes
```
python -m pytest -q
```

## Executar um programa
```
python -m src.interpreter exemplos/programa_valido.ml
python -m src.interpreter exemplos/programa_invalido.ml
```

## Estrutura
- `src/`: lexer, parser, AST e interpretador
- `tests/validos/` e `tests/invalidos/`: suíte de testes
- `exemplos/`: programas MiniLang de demonstração
- `docs/`: gramática, relatório, diário de bordo e vídeo

## Status
- [x] Lexer
- [x] Nós da AST
- [x] Parser
- [x] Interpretador
