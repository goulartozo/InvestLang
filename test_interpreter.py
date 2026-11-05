
from src.lexer import lexer
from src.parse import parser
from src.interpreter import Interpreter

with open(
    "examples/carteira.inv",
    "r",
    encoding="utf-8"
) as file:

    codigo = file.read()

ast = parser.parse(codigo, lexer=lexer)

if ast:
    interpreter = Interpreter(ast)
    resultado = interpreter.execute()
else:
    print("Não foi possível interpretar o código.")
