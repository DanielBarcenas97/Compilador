import re
from tokens import Token

#    El Lexer se encarga de buscar los tokens, los identifica con el uso de ER.
#	Se quita la parte de la cadena que hace match y se llama de manera recursiva a la funcion

def Lexer(linea,tokens = []):
	id_regex = '\\(*[A-Za-z][A-Za-z0-9]*\\)*' #Expresion Regular utilizada para buscar los Keywords
	num_regex = '\\d+'							#Expresion Regular utilizada para buscar numeros
	caracter = "^({|}|\\(|\\)|;|-|!|~|\\+|\\/|\\*)" #Expresion Regular utilizada para buscar tokens singulares
	
	linea = linea.lstrip() #quitando espacios al inicio de la cadena
	if(len(linea)==0):  #si la cadena es vacia entonces regresa true.
		return [True]

	if(re.match(id_regex, linea)):  #Checando si una parte de la cadena hace match
		id = re.match(id_regex, linea) #guardamos el token
		tokens.append([keyWords(id.group(0)),id.group(0)]) #Agregando el token a la lista de tokens ["Keyword etiqutado", "Valor contenido"]
		result = Lexer(linea.lstrip(id.group(0)),tokens) #Elimina el token encontrado  del inicio de la cadena

	elif(re.match(num_regex,linea)):#Checando si una parte de la cadena hace match
		numero = re.match(num_regex,linea) 
		tokens.append(['Int',numero.group(0)])
		result = Lexer(linea.lstrip(numero.group(0)),tokens)

	elif(re.match(caracter,linea)):#Checando si una parte de la cadena hace match
		special_char = re.match(caracter,linea)
		tok = singularTokens(special_char.group(0))
		tokens.append([tok,Token[tok].value])
		result = Lexer(linea[1:len(linea)],tokens)
	else:
		return ["ErrorLexico: " + linea[0] + " No es Aceptado."]
	return tokens

#Proceso de etiquetamiento. KeyWords recibe un  token de  la ER para identificadores regresa la etiqueta del token
def keyWords(token):
	if(token == Token.ReturnKeyword.value):
		return Token.ReturnKeyword.name
	elif(token == Token.IntKeyword.value):
		return Token.IntKeyword.name
	elif(token == Token.CharKeyword.value):
		return Token.CharKeyword.name
	else:	
		return 'Id'

#Recibe un caracter y valida si se encuentra definido en los tokens.
def singularTokens(token):
	if(token == "{"):
		return Token.OpenBrace.name
	elif(token == "}"):
		return Token.CloseBrace.name
	elif(token == "("):
		return Token.OpenParen.name
	elif(token == ")"):
		return Token.CloseParen.name
	elif(token == ";"):
		return Token.Semicolon.name
	elif(token == "~"):
		return Token.BitwiseComplement.name
	elif(token == "!"):
		return Token.LogicalNegation.name
	elif(token == "+"):
		return Token.Plus.name
	elif(token == "-"):
		return Token.Minus.name
	elif(token == "*"):
		return Token.Multiplication.name
	elif(token == "/"):
		return Token.Division.name
