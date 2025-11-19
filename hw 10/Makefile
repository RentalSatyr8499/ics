all:
	nasm -g -f elf64 -oprint.o print.s
	gcc -c part1.c
	gcc -o part1 part1.o print.o