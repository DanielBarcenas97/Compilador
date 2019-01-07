#!/bin/bash
echo '            Pruebas primer semana                 '
echo '****************** Válidas ***********************'

for i in "multi_digit" "newlines" "no_newlines" "return_0" "return_2" "spaces"
do
	python3 main.py ../test_codes/stage_1/valid/$i.c
done

echo

echo '***Inválidas***'
for i in "missing_paren" "wrong_case" "missing_retval" "no_brace" "no_semicolon" "no_space" 
do
	python3 main.py ../test_codes/stage_1/invalid/$i.c
done


echo '\-------------Pruebas segunda semana--------------/'
echo '****************** Válidas ***********************'
for i in "bitwise" "bitwise_zero" "neg" "nested_ops" "nested_ops_2" "not_five" "not_zero"
do
	python3 main.py ../test_codes/stage_2/valid/$i.c
done


echo '****************** Inválidas ****************** '
for i in "missing_const" "missing_semicolon" "nested_missing_const" "wrong_order" 
do
	python3 main.py ../test_codes/stage_2/invalid/$i.c
done


echo '\-------------Pruebas tercer semana--------------/'
echo '****************** Válidas ***********************'
for i in "add" "associativity" "associativity_2" "div" "mult" "parens" "precedence" "sub" "sub_neg" "unop_add" "unop_parens"
do
	python3 main.py ../test_codes/stage_3/valid/$i.c
done


echo '****************** Inválidas ****************** '
for i in "malformed_paren" "missing_first_op" "missing_second_op" "no_semicolon" 
do
	python3 main.py ../test_codes/stage_3/invalid/$i.c
done



