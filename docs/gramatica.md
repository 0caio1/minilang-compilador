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

_A fazer: derivar dos padrões acima (estados, alfabeto, transições)._

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
