import sys
from tokens import Token
from lexer import *
from parser import *
from generator import *

with open(sys.argv[1],"r") as f:
	linea = f.read()

print('\n\nProbando con ' + sys.argv[1])
#print('\n\nProbando con ' + linea)


tokens = Lexer(linea)
print("******************    Tokens    *************************")
print(tokens)

print('\-------------------------------------------------------------------------')
ast = program(tokens)	
print("\------------------------------------AST--------------------------------")
imprime(ast)
print("\-----------------------------------------------------------------------")
print(genera(ast[0]))