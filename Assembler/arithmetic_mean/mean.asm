section .data
    x dq 5, 3, 2, 6, 1, 7, 4
    y dq 0, 10, 1, 9, 2, 8, 5
    
    len dq ($ - x) / 16
    format db "%lf", 10, 0

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

calculate:
    movq xmm0, rdi
    mov rcx, rdx
    cvtsi2sd xmm0, rax
    cvtsi2sd xmm1, rcx
    mov rdx, 0
    divsd xmm0, xmm1

print:
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