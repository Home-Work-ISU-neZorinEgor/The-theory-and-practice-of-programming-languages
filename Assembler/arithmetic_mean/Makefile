all: run clean

run: mean 
	@./mean

mean: mean.o
	@gcc -no-pie -fno-pie -o mean mean.o

mean.o: mean.asm
	@nasm -f elf64 mean.asm -o mean.o

clean:
	@rm -f mean mean.o