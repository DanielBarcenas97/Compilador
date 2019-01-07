#!/bin/bash

echo 'Compilador'
if [[ $# > 0 ]]; then
	python3 main.py $1
	gcc assembly.s -o out
	echo 'El resultado del ejecutable es:'
	./out
	echo $?
else
	echo "Error no hay archivos"
	exit 1

fi

