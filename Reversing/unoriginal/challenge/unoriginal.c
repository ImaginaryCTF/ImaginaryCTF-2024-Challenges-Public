#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
  char buf[42];
  printf("Enter your flag here: ");
  gets(buf);
  for (int i=0; i<48; i++) {
    buf[i] ^= 5;
  }
  if (strcmp(buf, "lfqc~opvqZdkjqm`wZcidbZfm`fn`wZd6130a0`0``761gdx") == 0) {
    puts("Correct!");
    return 0;
  }
  else {
    puts("Incorrect.");
    return 0;
  }
}
