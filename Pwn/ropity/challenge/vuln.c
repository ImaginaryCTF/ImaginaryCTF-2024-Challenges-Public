#include <stdio.h>
#include <unistd.h>

void main() {
  char buf[8];
  fgets(buf, 0x100, stdin);
}

void printfile(char*file) {
  __asm__(
    ".intel_syntax noprefix\n"
    "mov rax, 2\n"
    "mov rsi, 0\n"
    "syscall\n"
    "mov rsi, rax\n"
    "mov rdi, 1\n"
    "mov rdx, 0\n"
    "mov r8, 0x100\n"
    "mov rax, 40\n"
    "syscall\n"
  );
}
