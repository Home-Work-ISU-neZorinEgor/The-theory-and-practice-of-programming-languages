section .data
    num dd 255.0
    format_sqrt db "approximate square root: %f", 0xA

section .text
    global main
    extern printf

main:
    push rax
    push rbx
    push rcx
    push rdx
    push rbp

    fld dword [num]
    fsqrt
    fstp qword [res1]

    ; Вывод квадратного корня
    mov rdi, format_sqrt
    mov rax, 1
    movq xmm0, [res1] 
    call printf

    pop rbp
    pop rdx
    pop rcx
    pop rbx
    pop rax

    mov rax, 60
    xor rdi, rdi
    syscall

section .bss
    res1 resq 1
