#include <stdio.h>
#include <unistd.h>

void main() {
  char *buf;
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  printf("%p\n> ", printf);
  scanf("%p%*c", &buf);
  fgets(buf, 0x300, stdin);
  puts("bye");
}

