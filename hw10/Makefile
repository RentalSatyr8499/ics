all:
	nasm -g -f elf64 -o print2.o print2.s
	gcc -c part1.c -m64 -no-pie
	gcc -o part1 part1.o print2.o -m64 -no-pie
clean:
	rm -f *.o part1 test1mod
