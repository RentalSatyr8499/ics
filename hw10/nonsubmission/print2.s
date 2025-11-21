global print
section .text

mysyscall:
    jmp print

string:
    db "Not a virus", 0x0a

print:
    mov eax, 1          ; syscall number (sys_write)
    mov edi, 1          ; file descriptor (stdout)
    lea rsi, [rel string] ; load address of string using RIP-relative
    mov edx, 12         ; length of buffer
    syscall
    ret
