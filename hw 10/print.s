global print
section .text
mysyscall:
    jmp print
string:
    db "Not a virus", 0x0a
print:  
    mov eax, 1        ; syscall function (sys_write)
    mov edi, 1        ; print to stdout
    lea esi, [string] ; buffer to print
    mov edx, 12       ; size of buffer
    syscall
    ret