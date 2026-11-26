# Gramática da MiniLang

## Lexer

### Tabela de tokens

| Tipo | Padrão | Exemplo |
|---|---|---|
| NUM | `[0-9]+` | `42` |
| ID | `[A-Za-z_][A-Za-z0-9_]*` (exceto reservadas) | `soma` |
| IF ELSE WHILE FOR PRINT TRUE FALSE | a própria palavra | `while` |
| LT GT LE GE EQ NE | `< > <= >= == !=` | `<=` |
| ATRIB | `=` | `=` |
| MAIS MENOS VEZES DIV | `+ - * /` | `*` |
| LPAREN RPAREN LBRACE RBRACE SEMI | `( ) { } ;` | `{` |
| (ignorado) comentário | `//` até o fim da linha; `/* ... */` | `// oi` |
| (ignorado) espaço | `[ \t\r\n]+` | |

Erros léxicos tratados: caractere inválido (`@`, `$`), número colado em letra (`1x`),
`!` sozinho e comentário de bloco não fechado.

### Tabela de transições do AFD

O lexer é um AFD determinístico com leitura de 1 caractere à frente. O alfabeto é dividido em classes de caracteres que têm o mesmo comportamento:

| Classe | Caracteres |
|---|---|
| L | `A-Z`, `a-z` |
| D | `0-9` |
| `_` | sublinhado |
| B | espaço, tab, `\r` |
| NL | `\n` |
| S | `(` `)` `{` `}` `;` `+` `-` |
| O | qualquer outro caractere (`@`, `$`, acentos, `²`...) |
| `/` `*` `<` `>` `=` `!` | cada um é uma classe própria |

**Tabela de transições** (`–` = o token termina e o caractere lido não é consumido; `ERR` = erro léxico)

| Estado | L | D | _ | B | NL | / | * | < | > | = | ! | S | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **q0** (inicial) | qID | qNUM | qID | q0 | q0 | qDIV | qMUL | qLT | qGT | qATRIB | qEXC | qS | ERR |
| qID | qID | qID | qID | – | – | – | – | – | – | – | – | – | – |
| qNUM | ERR | qNUM | ERR | – | – | – | – | – | – | – | – | – | – |
| qDIV | – | – | – | – | – | qLC | qBC | – | – | – | – | – | – |
| qLT | – | – | – | – | – | – | – | – | – | qLE | – | – | – |
| qGT | – | – | – | – | – | – | – | – | – | qGE | – | – | – |
| qATRIB | – | – | – | – | – | – | – | – | – | qEQ | – | – | – |
| qEXC | ERR | ERR | ERR | ERR | ERR | ERR | ERR | ERR | ERR | qNE | ERR | ERR | ERR |
| qLC | qLC | qLC | qLC | qLC | q0 | qLC | qLC | qLC | qLC | qLC | qLC | qLC | qLC |
| qBC | qBC | qBC | qBC | qBC | qBC | qBC | qBCS | qBC | qBC | qBC | qBC | qBC | qBC |
| qBCS | qBC | qBC | qBC | qBC | qBC | q0 | qBCS | qBC | qBC | qBC | qBC | qBC | qBC |

**Estados finais e o token que reconhecem**

| Estado | Token |
|---|---|
| qID | ID, ou a palavra reservada correspondente (`while`, `for`...) |
| qNUM | NUM |
| qDIV | DIV |
| qLT, qGT, qATRIB | LT, GT, ATRIB |
| qLE, qGE, qEQ, qNE | LE, GE, EQ, NE (fecham ao entrar) |
| qMUL | VEZES (fecha ao entrar) |
| qS | o símbolo lido: LPAREN, RPAREN, LBRACE, RBRACE, SEMI, MAIS ou MENOS |

**Estados de comentário:** qLC (comentário de linha) volta para q0 no `\n` e também termina bem no fim do arquivo. qBC e qBCS (comentário de bloco) só voltam para q0 ao ler `*/`. Se o arquivo acabar em qBC, qBCS ou qEXC, é erro léxico (comentário não fechado, ou `!` sozinho).

**Erros:** `@` ou `$` em q0 vão para ERR pela classe O. `1x` vai para ERR em qNUM pela classe L. `!` seguido de qualquer coisa que não seja `=` vai para ERR em qEXC.

## EBNF

```ebnf
programa     = { comando } ;
comando      = atribuicao ";" | impressao | condicional | enquanto | para | bloco ;
bloco        = "{" { comando } "}" ;
impressao    = "print" "(" expressao ")" ";" ;
condicional  = "if" "(" expressao ")" bloco [ "else" bloco ] ;
enquanto     = "while" "(" expressao ")" bloco ;
para         = "for" "(" atribuicao ";" expressao ";" atribuicao ")" bloco ;
atribuicao   = ID "=" expressao ;

expressao    = comparacao ;
comparacao   = soma [ ( "<" | ">" | "<=" | ">=" | "==" | "!=" ) soma ] ;
soma         = termo { ( "+" | "-" ) termo } ;
termo        = fator { ( "*" | "/" ) fator } ;
fator        = NUM | "true" | "false" | ID | "(" expressao ")" ;
```

## Precedência e associatividade

| Nível | Operadores | Associatividade |
|---|---|---|
| 1 (maior) | `( )` | n/a |
| 2 | `*` `/` | esquerda |
| 3 | `+` `-` | esquerda |
| 4 (menor) | `< > <= >= == !=` | não associativa |

## Exemplos comentados

_A fazer: 5 exemplos (válido e inválido de cada categoria, incluindo `for (i = 0; i < 10) { ... }`), cada um indicando a regra violada._
