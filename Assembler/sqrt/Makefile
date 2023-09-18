all: run clean

run: sqrt 
	@./sqrt

sqrt: sqrt.o
	@gcc -no-pie -fno-pie -o sqrt sqrt.o

sqrt.o: sqrt.asm
	@nasm -f elf64 sqrt.asm -o sqrt.o

clean:
	@rm -f sqrt sqrt.o
