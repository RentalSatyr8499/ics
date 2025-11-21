all:
	nasm -g -f elf64 -o print.o print.s
	gcc -c part1.c -m64 -no-pie
	gcc -o part1 part1.o print.o -m64 -no-pie
clean:
	rm -f *.o part1 test1mod testAmod testBmod
