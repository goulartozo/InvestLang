
import ply.yacc as yacc

try:
    from .lexer import tokens, lexer
except ImportError:
    from lexer import tokens, lexer


# ==========================================
# GRAMÁTICA DA INVESTLANG
# ==========================================

start = "program"


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def p_program(p):
    "program : carteira"
    p[0] = p[1]


def p_carteira(p):
    "carteira : CARTEIRA LBRACE statements RBRACE"
    p[0] = {
        "type": "carteira",
        "statements": p[3]
    }


# ==========================================
# LISTA DE DECLARAÇÕES
# ==========================================

def p_statements_recursive(p):
    "statements : statements statement"
    p[0] = p[1] + [p[2]]


def p_statements_empty(p):
    "statements : empty"
    p[0] = []


def p_empty(p):
    "empty :"
    p[0] = None


# ==========================================
# DECLARAÇÕES
# ==========================================

def p_statement(p):
    """statement : assignment
                 | section
                 | command
                 | conditional"""
    p[0] = p[1]


# ==========================================
# ATRIBUIÇÕES
# ==========================================

def p_assignment(p):
    "assignment : key ASSIGN value SEMICOLON"
    p[0] = {
        "type": "assignment",
        "name": p[1],
        "value": p[3]
    }


def p_key(p):
    """key : ID
           | NOME
           | PERFIL
           | OBJETIVO
           | HORIZONTE_TEMPORAL
           | CAPITAL_TOTAL
           | VOLATILIDADE_MAXIMA
           | TAXA_ADMINISTRATIVA_MAXIMA
           | ATIVO_MAXIMO
           | SETOR_MAXIMO
           | FREQUENCIA
           | TOLERANCIA
           | METODO"""
    p[0] = p[1]


# ==========================================
# VALORES
# ==========================================

def p_value_number(p):
    "value : NUMBER"
    p[0] = {
        "type": "number",
        "value": p[1]
    }


def p_value_percentage(p):
    "value : PERCENTAGE"
    p[0] = {
        "type": "percentage",
        "value": p[1]
    }


def p_value_string(p):
    "value : STRING"
    p[0] = {
        "type": "string",
        "value": p[1]
    }


def p_value_identifier(p):
    "value : ID"
    p[0] = {
        "type": "identifier",
        "value": p[1]
    }


def p_value_years(p):
    "value : NUMBER YEARS"
    p[0] = {
        "type": "years",
        "value": p[1]
    }


# ==========================================
# BLOCOS DA LINGUAGEM
# ==========================================

def p_section(p):
    "section : section_name LBRACE statements RBRACE"
    p[0] = {
        "type": "section",
        "name": p[1],
        "statements": p[3]
    }


def p_section_name(p):
    """section_name : ALOCACAO
                    | RESTRICOES
                    | CONCENTRACAO
                    | SETORIAL
                    | GEOGRAFICO
                    | REBALANCEAMENTO"""
    p[0] = p[1]


# ==========================================
# COMANDOS
# ==========================================

def p_command(p):
    """command : ANALISAR SEMICOLON
               | GERAR_RELATORIO SEMICOLON"""
    p[0] = {
        "type": "command",
        "name": p[1]
    }


def p_command_print(p):
    "command : IMPRIMIR LPAREN value RPAREN SEMICOLON"
    p[0] = {
        "type": "print",
        "value": p[3]
    }


# ==========================================
# ESTRUTURAS CONDICIONAIS
# ==========================================

def p_conditional(p):
    "conditional : SE LPAREN expression RPAREN LBRACE statements RBRACE"
    p[0] = {
        "type": "conditional",
        "condition": p[3],
        "statements": p[6]
    }


# ==========================================
# EXPRESSÕES RELACIONAIS
# ==========================================

def p_expression(p):
    "expression : key relational_operator value"
    p[0] = {
        "type": "expression",
        "left": p[1],
        "operator": p[2],
        "right": p[3]
    }


def p_relational_operator(p):
    """relational_operator : EQ
                           | NE
                           | LT
                           | GT
                           | LE
                           | GE"""
    p[0] = p[1]


# ==========================================
# TRATAMENTO DE ERROS SINTÁTICOS
# ==========================================

def p_error(p):
    if p:
        print(
            f"Erro sintático: token inesperado "
            f"'{p.value}' na linha {p.lineno}"
        )
    else:
        print("Erro sintático: fim inesperado do arquivo.")


# ==========================================
# CONSTRUÇÃO DO PARSER
# ==========================================

parser = yacc.yacc()


# ==========================================
# TESTE INICIAL
# ==========================================

if __name__ == "__main__":

    codigo = """
    carteira {
        nome = "Carteira Diversificada";
        perfil = "moderado";
        objetivo = "Crescimento patrimonial";
        horizonte_temporal = 5 anos;
        capital_total = 100000.00;

        alocacao {
            acoes_nacionais = 30%;
            acoes_internacionais = 20%;
            fundos_imobiliarios = 15%;
            fundos_multimercado = 10%;
            renda_fixa = 25%;
        }

        restricoes {
            volatilidade_maxima = 10%;
            taxa_administrativa_maxima = 2%;

            concentracao {
                ativo_maximo = 15%;
                setor_maximo = 30%;
            }

            setorial {
                tecnologia = 10%;
                financeiro = 5%;
                energia = 10%;
                saude = 10%;
                outros = 65%;
            }

            geografico {
                brasil = 50%;
                emergentes = 15%;
                desenvolvidos = 35%;
            }
        }

        rebalanceamento {
            frequencia = trimestral;
            tolerancia = 2%;
            metodo = proporcional;
        }

        se (capital_total < 1000) {
            imprimir("Capital abaixo do minimo definido");
        }

        analisar;
        gerar_relatorio;
    }
    """

    resultado = parser.parse(codigo, lexer=lexer)

    if resultado:
        print("\nAnálise sintática concluída!")
        print("\nÁrvore sintática:")
        print(resultado)
    else:
        print("\nNão foi possível construir a árvore sintática.")
