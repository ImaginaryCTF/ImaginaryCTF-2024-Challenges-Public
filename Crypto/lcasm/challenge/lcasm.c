#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <assert.h>
#include <string.h>
#include <sys/mman.h>

unsigned long readint(char* prompt) {
  unsigned long out;
  printf("%s", prompt);
  scanf("%lu%*c", &out);
  return out;
}

unsigned long mult(unsigned long long a, unsigned long long b, unsigned long long m) {
  __uint128_t r = (__uint128_t)a * b;
  r = r % m;
  return (unsigned long) r;
}

int main() {
    unsigned long * sc;
    unsigned long x, a, c, m;

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    sc = mmap(0, 0x1000, 7, MAP_ANONYMOUS | MAP_SHARED, 0, 0);

    x = readint("x> ");
    a = readint("a> ");
    c = readint("c> ");
    m = readint("m> ");

    for (int i=0; i<0x10; i++) {
      x = (mult(a,x,m) + c) % m;
      sc[i] = (unsigned long) x;
    }

    mprotect(sc, 0x1000, 5);
    ((void (*)()) sc)();
}
