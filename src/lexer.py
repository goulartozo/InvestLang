
import ast
import ply.lex as lex


# ==========================================
# PALAVRAS RESERVADAS
# ==========================================

reserved = {
    "carteira": "CARTEIRA",
    "nome": "NOME",
    "perfil": "PERFIL",
    "objetivo": "OBJETIVO",
    "horizonte_temporal": "HORIZONTE_TEMPORAL",
    "capital_total": "CAPITAL_TOTAL",

    "alocacao": "ALOCACAO",

    "restricoes": "RESTRICOES",
    "volatilidade_maxima": "VOLATILIDADE_MAXIMA",
    "taxa_administrativa_maxima": "TAXA_ADMINISTRATIVA_MAXIMA",

    "concentracao": "CONCENTRACAO",
    "ativo_maximo": "ATIVO_MAXIMO",
    "setor_maximo": "SETOR_MAXIMO",

    "setorial": "SETORIAL",
    "geografico": "GEOGRAFICO",

    "rebalanceamento": "REBALANCEAMENTO",
    "frequencia": "FREQUENCIA",
    "tolerancia": "TOLERANCIA",
    "metodo": "METODO",

    "analisar": "ANALISAR",
    "gerar_relatorio": "GERAR_RELATORIO",

    "se": "SE",
    "imprimir": "IMPRIMIR",

    "anos": "YEARS"
}


# ==========================================
# LISTA DE TOKENS
# ==========================================

tokens = [
    "ID",
    "STRING",
    "NUMBER",
    "PERCENTAGE",

    "ASSIGN",
    "EQ",
    "NE",
    "LT",
    "GT",
    "LE",
    "GE",

    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",

    "LBRACE",
    "RBRACE",
    "LPAREN",
    "RPAREN",
    "SEMICOLON",
    "COMMA",
] + list(reserved.values())


# ==========================================
# OPERADORES E DELIMITADORES
# ==========================================

t_EQ = r"=="
t_NE = r"!="
t_LE = r"<="
t_GE = r">="

t_ASSIGN = r"="
t_LT = r"<"
t_GT = r">"

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"

t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_SEMICOLON = r";"
t_COMMA = r","


# ==========================================
# LITERAIS
# ==========================================

def t_PERCENTAGE(t):
    r"\d+(\.\d+)?%"
    t.value = float(t.value[:-1])
    return t


def t_NUMBER(t):
    r"\d+(\.\d+)?"
    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = ast.literal_eval(t.value)
    return t


# ==========================================
# IDENTIFICADORES E PALAVRAS RESERVADAS
# ==========================================

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, "ID")
    return t


# ==========================================
# COMENTÁRIOS
# ==========================================

def t_COMMENT_BLOCK(t):
    r"/\*[\s\S]*?\*/"
    t.lexer.lineno += t.value.count("\n")


def t_COMMENT_LINE(t):
    r"//[^\n]*"
    pass


# ==========================================
# CONTROLE DE LINHAS E ESPAÇOS
# ==========================================

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


t_ignore = " \t\r"


# ==========================================
# TRATAMENTO DE ERROS
# ==========================================

def t_error(t):
    print(
        f"Erro léxico: caractere inesperado "
        f"'{t.value[0]}' na linha {t.lexer.lineno}"
    )
    t.lexer.skip(1)


# ==========================================
# CONSTRUÇÃO DO ANALISADOR
# ==========================================

lexer = lex.lex()


# ==========================================
# TESTE INICIAL
# ==========================================

if __name__ == "__main__":

    codigo = '''
    carteira {
        nome = "Carteira Diversificada";
        capital_total = 100000.00;

        alocacao {
            acoes_nacionais = 30%;
            renda_fixa = 25%;
        }

        // Comentário de teste
        analisar;
    }
    '''

    lexer.input(codigo)

    print("TOKENS RECONHECIDOS:")
    print("--------------------")

    for token in lexer:
        print(
            f"Tipo: {token.type:<25} "
            f"Valor: {token.value}"
        )
