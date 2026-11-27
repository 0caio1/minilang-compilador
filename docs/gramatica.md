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

## Regras semânticas (interpretador)

| Regra | Se for violada |
|---|---|
| Há dois tipos: inteiro e booleano | — |
| Variável precisa ser atribuída antes de ser usada | erro semântico |
| `+ - * /` e `< > <= >=` só aceitam inteiros | erro semântico |
| `==` e `!=` só comparam valores do mesmo tipo | erro semântico |
| `/` é divisão inteira truncada em direção a zero: `(0 - 7) / 2` dá `-3` | divisão por zero é erro semântico |
| A condição de `if`, `while` e `for` precisa ser booleana | erro semântico |
| Uma única tabela de símbolos global (escopo aninhado está fora do escopo do projeto): bloco não cria escopo, e a variável do `for` continua existindo depois do laço | — |
| Cada laço repete no máximo 10.000 vezes | erro de execução (provável laço infinito) |
| `print` mostra booleanos como `true` / `false` | — |

## Exemplos comentados

### Exemplo 1: programa válido

```
x = 3;
while (x > 0) {
  print(x);
  x = x - 1;
}
soma = 0;
for (i = 0; i < 5; i = i + 1) {
  soma = soma + i;
}
```

**Por que é válido:** segue todas as regras da gramática. O `while` tem condição entre parênteses e um bloco, e o `for` tem as três cláusulas (inicialização, condição e atualização) separadas por `;`. Todas as variáveis estão definidas antes do uso e as condições são booleanas.

### Exemplo 2: inválido léxico

```
x = 5 @ 3;
```

**Por que é inválido:** o caractere `@` não pertence ao conjunto de símbolos reconhecidos pelo lexer da linguagem. Como não existe um token correspondente a esse caractere na especificação léxica, o analisador léxico identifica um erro e interrompe a análise. Na tabela de transições, o `@` pertence à classe O, e a transição de q0 com a classe O leva a ERR.

### Exemplo 3: inválido sintático

```
x = (1 + ;
```

**Por que é inválido:** o lexer aceita, porque todos os símbolos existem. O erro aparece no parser. Depois do `(`, a regra `fator` pede uma expressão. A expressão lê `1`, e o `+` exige um `termo` em seguida (regra `soma`). Mas o próximo token é `;`, e a regra `fator` só aceita `NUM`, `true`, `false`, `ID` ou `(`. Então a regra `fator` é violada.

### Exemplo 4: inválido sintático (laço mal formado)

```
for (i = 0; i < 10) { print(i); }
```

**Por que é inválido:** o parser identifica que a estrutura do `for` está incompleta. De acordo com a regra `para` da gramática, o comando `for` exige três cláusulas entre parênteses: inicialização, condição e atualização, separadas por dois pontos e vírgulas. No exemplo, falta a cláusula de atualização (por exemplo, `i = i + 1`) e o segundo ponto e vírgula. O parser lê a condição `i < 10` e espera um `;`, mas encontra `)`. Portanto, a estrutura não corresponde à regra sintática do `for`.

### Exemplo 5: inválido semântico

```
while (1 + 2) { print(1); }
```

**Por que é inválido:** a condição do `while` deve ser uma expressão que resulte em booleano (como `x > 0` ou `true`). No exemplo, a expressão `1 + 2` resulta em um valor numérico, e não booleano. Embora a estrutura esteja sintaticamente correta, ocorre um erro na análise semântica devido à incompatibilidade de tipos entre a condição esperada e o valor fornecido. Esse erro é detectado pelo interpretador, na execução, e não pelo parser.
