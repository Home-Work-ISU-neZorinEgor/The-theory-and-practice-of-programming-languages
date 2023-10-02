section .bss
    resb 8  ; Этот резервирует 8 байтов для rdi

section .text
    global main
    extern printf

main:

read_data:
    xor rax, rax    ; sum
    xor rdx, rdx    ; index
    xor rsi, rsi    ; item

read_loop:
    cmp rdx, [len]
    jge calculate
    mov rsi, [x + rdx * 8]
    sub rsi, [y + rdx * 8]

iterate:
    add rax, rsi
    add rdx, 1
    jmp read_loop

print:
    movq xmm0, rax
    push rax
    push rbx
    push rcx
    push rdx
    push rbp

    mov rdi, format
    mov rax, 1
    call printf
    
    pop rdx
    pop rcx
    pop rbx
    pop rax
    pop rbp

end:
    ret
    xor rdx, rdx
    xor rsi, rsi
    xor rbp, rbp
    mov rax, 60
    xor rdi, rdi
    syscall
