all:
	sage generate_program.sage
	gcc -Wall -Wextra -Wpedantic -O0 -o svm_revenge svm_revenge.c
	strip svm_revenge
	./svm_revenge
