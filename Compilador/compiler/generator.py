def genera(ast):
	file_assembly = open('assembly.s','w+')
	if(type(ast)!=bool):
		if(len(ast)==2 and type(ast[1]) != list):  #hoja de ast
			cons = ast[1] 
			file_assembly.write('movl    $'+cons+', %eax')
			return 'movl    $'+cons+', %eax'
		elif(len(ast)==2):  #nodo solo con un hijo
			expr = genera(ast[1])
			if(ast[0] == 'Function'):
				file_assembly.write('.globl _'+ast[1][0]+'\n_'+ast[1][0]+':\n' + expr)
				return  '.globl _'+ast[1][0]+'\n_'+ast[1][0]+':\n' + expr
			if(ast[0] == 'return' ):
				file_assembly.write(expr+'\nret')
				return  expr+'\nret' 
			if(ast[0][0] == 'UnaryOp' and type(expr) == str):
				file_assembly.write(expr + my_unary_op(ast[0][1]))
				return expr + my_unary_op(ast[0][1])
			file_assembly.write(expr)
			return expr
		elif(len(ast)==3): #nodo con dos hijos
			term1 = ast[1] if type(ast[1]) != list else genera(ast[1])	
			op = ast[0][1]
			term2 = ast[2] if type(ast[2]) != list else genera(ast[2])
			file_assembly.write(this_is_my_op(term1,op,term2))
			return this_is_my_op(term1,op,term2)


def this_is_my_op(op1,sign,op2):
	expr = ''
	if(sign == 'Multiplication'):
		expr = op1 + '\npush %eax\n'+op2+'\npop %ecx\nimul %ecx, %eax'
	elif(sign == 'Plus'):
		expr = op1 + '\npush %eax\n'+op2+'\npop %ecx\naddl %ecx, %eax'
	elif(sign == 'Division'):
		expr = '\nmov %edx, 0\n'+op1+'\npush %eax\n'+op2+'\npop %ecx\ndiv %ecx'
	elif(sign == 'Minus'):
		expr = op1 + '\npush %eax\n'+op2+'\npop %ecx\nsub %ecx, %eax'
	return expr

def my_unary_op(op):
	exp = ''
	if(op == 'LogicalNegation'):
		exp = '\nmpl   $0, %eax\nmovl   $0, %eax\nsete   %al'
	else:
		exp = '\nneg     %eax' 
	return exp
