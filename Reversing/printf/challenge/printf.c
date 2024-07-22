#include <stdio.h>
#include <stdlib.h>

long stack[1024];
int sp = 0;
long regs[8];
unsigned long buf[0x200];

int func() {
  return 1 ;
}

void inp() {
  stack[++sp] = getchar();
}

void pr() {
  putchar(stack[sp]);
}

int pushi(long trash, long* arg) {
  stack[++sp] = arg[0];
  return 1;
}

int pushr(long trash, long* arg) {
  unsigned long reg;
  asm ( "bsr %1, %0\n"
      : "=r"(reg)
      : "r" ((arg[1] & 0xff00000000) >> 32)
  );
  stack[++sp] = regs[reg];
  return 1;
}

int pop(long trash, long* arg) {
  unsigned long reg;
  asm ( "bsr %1, %0\n"
      : "=r"(reg)
      : "r" ((arg[1] & 0xff00000000) >> 32)
  );
  regs[reg] = stack[sp--];
  return 1;
}

int add(long trash, long* arg) {
  unsigned long reg;
  asm ( "bsr %1, %0\n"
      : "=r"(reg)
      : "r" ((arg[1] & 0xff00000000) >> 32)
  );
  regs[reg] = stack[sp] + stack[sp-1];
  return 1;
}

int sub(long trash, long* arg) {
  unsigned long reg;
  asm ( "bsr %1, %0\n"
      : "=r"(reg)
      : "r" ((arg[1] & 0xff00000000) >> 32)
  );
  regs[reg] = stack[sp] - stack[sp-1];
  return 1;
}

int mul(long trash, long* arg) {
  unsigned long reg;
  asm ( "bsr %1, %0\n"
      : "=r"(reg)
      : "r" ((arg[1] & 0xff00000000) >> 32)
  );
  regs[reg] = stack[sp] * stack[sp-1];
  return 1;
}

int idiv(long trash, long* arg) {
  unsigned long reg;
  asm ( "bsr %1, %0\n"
      : "=r"(reg)
      : "r" ((arg[1] & 0xff00000000) >> 32)
  );
  regs[reg] = stack[sp] / stack[sp-1];
  return 1;
}

int mod(long trash, long* arg) {
  unsigned long reg;
  asm ( "bsr %1, %0\n"
      : "=r"(reg)
      : "r" ((arg[1] & 0xff00000000) >> 32)
  );
  regs[reg] = stack[sp] % stack[sp-1];
  return 1;
}

int xor(long trash, long* arg) {
  unsigned long reg;
  asm ( "bsr %1, %0\n"
      : "=r"(reg)
      : "r" ((arg[1] & 0xff00000000) >> 32)
  );
  regs[reg] = stack[sp] ^ stack[sp-1];
  return 1;
}

int ex(long trash, long* arg) {
  if (regs[0] != 0)
    _exit(0);
  return 1;
}

/*
void debug(long trash, long* arg) {
  unsigned long reg;
  asm ( "bsr %1, %0\n"
      : "=r"(reg)
      : "r" ((arg[1] & 0xff00000000) >> 32)
  );
  printf("%p %p %p\n", arg[0], arg[1], reg);
  printf("%p %p %p %p %p %p %p %p\n", regs[0], regs[1], regs[2], regs[3], regs[4], regs[5], regs[6], regs[7]);
}
*/

void __attribute__ ((constructor)) init() {
  // i have no idea why it works this way.
  buf[320] = (unsigned long) &inp;
  buf[321] = (unsigned long) &inp;
  buf[322] = (unsigned long) &pr;
  buf[324] = (unsigned long) &pop;
  buf[325] = (unsigned long) &pop;
  buf[326] = (unsigned long) &add;
  buf[327] = (unsigned long) &sub;
  buf[328] = (unsigned long) &mul;
  buf[329] = (unsigned long) &idiv;
  buf[330] = (unsigned long) &mod;
  buf[331] = (unsigned long) &xor;
  buf[333] = (unsigned long) &pushi;
  buf[334] = (unsigned long) &pushr;
  buf[344] = (unsigned long) &ex;
  buf[320-255] = (unsigned long) &func;
  buf[321-255] = (unsigned long) &func;
  buf[324-255] = (unsigned long) &func;
  buf[325-255] = (unsigned long) &func;
  buf[326-255] = (unsigned long) &func;
  buf[327-255] = (unsigned long) &func;
  buf[328-255] = (unsigned long) &func;
  buf[329-255] = (unsigned long) &func;
  buf[330-255] = (unsigned long) &func;
  buf[333-255] = (unsigned long) &func;
  buf[334-255] = (unsigned long) &func;
  buf[344-255] = (unsigned long) &func;

  unsigned long * arginfo = (unsigned long*)((unsigned char*)&printf + 0x1ba140);
  unsigned long * function = (unsigned long*)((unsigned char*)&printf + 0x1bb258);
  *arginfo = buf;
  *function = (unsigned long*)(((unsigned char*)buf)+0x800);
}

int main() {
/*
  register_printf_specifier('A', inp, func);
  register_printf_specifier('B', pr, func);
  register_printf_specifier('M', pushi, func);
  register_printf_specifier('N', pushr, func);
  register_printf_specifier('E', pop, func);
  register_printf_specifier('F', add, func);
  register_printf_specifier('G', sub, func);
  register_printf_specifier('H', mul, func);
  register_printf_specifier('I', idiv, func);
  register_printf_specifier('J', mod, func);
  register_printf_specifier('K', xor, func);
  register_printf_specifier('X', ex, func);
//  register_printf_specifier('?', debug, func);
*/
  printf("
