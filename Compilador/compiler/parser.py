from tokens import *
import sys

"""
	<program> ::= <function>
	<function> ::= "int" <id> "(" ")" "{" <statement> "}"
	<statement> ::= "return" <exp> ";"
	<exp> ::= <int>

"""
class ErrorSintactico(RuntimeError):
	def __init__(self, token_inesperado,esperado):
		self.informacion = 'Error sintáctico, token inesperado ' + token_inesperado + ' Se esperaba ' + esperado

#El Parseo es recursivo, si un token genera un error retornara un False y si esta correcto retorna el AST. 
def program(tokens, ast = []):
	result = parse_function_declaration(tokens,ast)
	#print(type(result))
	#print(ErrorSintactico)
	if(type(result) != ErrorSintactico):
		ast.append(result)
		return ast		
	else: 
		return result

##<class 'list'>  !=  <class 'Error.ErrorSintactico'>

#Parsea la estructura de una funcion
def parse_function_declaration(tokens,ast):
	nodo = []
	tk = tokens.pop(0)
	if(tk[0] != Token.IntKeyword.name and tk[0] != Token.CharKeyword.name): #int #main
		#return ErrorSintactico(tk,Token.IntKeyword.name) #Se envia el token que esta mal y el esperado.
		print("Error Sintactico: \n  Token inesperado " + tk + "Se esperaba " + Token.IntKeyword.name + "\n")
		sys.exit()
	tk = tokens.pop(0) if len(tokens) > 0 else ['']
	#------------------------ Se busca el tk[0] que sea igual al id
	if(tk[0] != 'Id'):
		print("Error Sintactico: \n  Token inesperado " + tk[1] + "Se esperaba " + 'Identifier' + "\n");
		sys.exit()
		#return ErrorSintactico(tk[1],'Identifier')
	nodo.append(tk[1])

	tk = tokens.pop(0) if len(tokens) > 0 else ['']
	if(tk[0] != Token.OpenParen.name):
		print("Error Sintactico: \n  Token inesperado " + tk[0] + "Se esperaba " + Token.OpenParen.name +"\n")
		sys.exit()
	#	return ErrorSintactico(tk[0],Token.OpenParen.name) #(

	tk = tokens.pop(0) if len(tokens) > 0 else ['']
	if(tk[0] != Token.CloseParen.name):
		print("Error Sintactico: \n  Token inesperado " + tk[0] + "Se esperaba " + Token.CloseParen.name + "\n")
		sys.exit()
	tk = tokens.pop(0) if len(tokens) > 0 else ['']
	if(tk[0] != Token.OpenBrace.name):
		print("Error Sintactico: \n  Token inesperado " + tk[0] + "Se esperaba " + Token.OpenBrace.name + "\n")
		sys.exit()
		#return ErrorSintactico(tk[0],Token.OpenBrace.name) #{

	result = parse_statement(tokens,ast) # se llama a parse_statement para buscar una expresion valida
	if(type(result) == ErrorSintactico):              #si regresa false, en la lista, entonces no encontró algo válido
		return result						
	nodo.append(['Statement',result])					  #si encontró algo válido lo agrego al nodo 'function'	

	tk = tokens.pop(0) if len(tokens) > 0 else ['']
	if(tk[0] != Token.CloseBrace.name):
		print("Error Sintactico: \n  Token inesperado " + tk[0] + "Se esperaba " + Token.CloseBrace.name + "\n")
		sys.exit();
		#return ErrorSintactico(tk[0],Token.CloseBrace.name) #}
	return(['Function',nodo]) # se retorna el nodo funcion

#parsea la estructura de un statement
def parse_statement(tokens,ast):
	nodo = []	
	tk = tokens.pop(0)
	if(tk[0] != Token.ReturnKeyword.name): #return
		print("Error Sintactico: \n  Token inesperado " + tk[0] + "Se esperaba " + Token.ReturnKeyword.name + "\n")
		sys.exit()
		#return ErrorSintactico(tk[0],Token.ReturnKeyword.name)
	nodo.append(tk[1])

	result = parse_expresion(tokens)  #se busca encontrar una expresion válida, si no retorna false
	if(type(result) == ErrorSintactico):		  #implica que sí encontró un nodo 'expresion' y se agrega al nodo 'statement'
		return result
	nodo.append(result)
	tk = tokens.pop(0)
	if(tk[0] != Token.Semicolon.name): #;
		print("Error Sintactico: \n  Token inesperado " + tk[0] + "Se esperaba " + Token.Semicolon.name + "\n");
		sys.exit()
		#return ErrorSintactico(tk[0],Token.Semicolon.name)
	return nodo #se retorna el nodo statement

#parsea la estructura de una expresion
def parse_factor(tokens):
	tk = tokens.pop(0)
	if(tk[0] == 'Int'):
		return ['Constant',tk[1]]  #busca que la expresion sea un int, sino, retorna false
	elif(tk[0] == Token.Minus.name or tk[0] == UnaryOp.BitwiseComplement.name or tk[0] == UnaryOp.LogicalNegation.name):
		result = parse_factor(tokens)
		if(type(result) != ErrorSintactico):
			my_node = [['UnaryOp',tk[0]],result]
			return my_node
		else:
			return result
	elif(tk[0] == Token.OpenParen.name):
		result = parse_expresion(tokens)
		if(type(result) != ErrorSintactico):
			tk = tokens.pop(0)
			if(tk[0] == Token.CloseParen.name):
				my_node = result
				return my_node
			else:
				print("Error Sintactico: \n  Token inesperado " + tk + "Se esperaba " + Token.CloseParen.name + "\n")
				sys.exit()
				#return ErrorSintactico(tk,Token.CloseParen.name)
		else:
			sys.exit()
			#return result
	else:
		print("Error Sintactico: \n  Token inesperado " + tk[0] + "Se esperaba" + " Const  \n" )
		sys.exit()
		#return ErrorSintactico(tk[0],'Const')


def parse_expresion(tokens):
	term = parse_term(tokens)
	if(type(term) != ErrorSintactico):
		my_exp = ['Expresion']
		while(True):
			if(tokens[0][0] == BinaryOp.Addition.value.name or tokens[0][0] == BinaryOp.Subtraction.value.name):
				tk = tokens.pop(0)
				other_term = parse_term(tokens)
				if(type(other_term) != ErrorSintactico):
					term = [["BinaryOp",BinaryOp.Addition.value.name] if (tk[0] == BinaryOp.Addition.value.name) else ["BinaryOp",BinaryOp.Subtraction.value.name],term,other_term]
				else:
					return other_term
			else: 
				return ['Expresion',term]
				break
	else:
		return term

def parse_term(tokens):
	factor = parse_factor(tokens)
	if(type(factor) != ErrorSintactico):
		my_term = ['Term']
		while(True):
			#tk = tokens.pop(0)
			if(tokens[0][0] == BinaryOp.Multiplication.value.name or tokens[0][0] == BinaryOp.Division.value.name):
				tk = tokens.pop(0)
				other_factor = parse_factor(tokens)
				if(type(other_factor) != ErrorSintactico):
					factor = [["BinaryOp",BinaryOp.Multiplication.value.name] if (tk[0] == BinaryOp.Multiplication.value.name) else ["BinaryOp",BinaryOp.Division.value.name],['Factor',factor],['Factor',other_factor]]
				else:
					return other_factor
			else: 
				return ['Term',factor]
				break
	else:
		return factor




#imprime ast en pretty mode
def imprime(nodes,level = 1):
	for l in nodes:
		if(type(l) is list):
			imprime(l,level + 2)
		else:
			print("|"+'-'*(level-1)+"-"*level+l)

