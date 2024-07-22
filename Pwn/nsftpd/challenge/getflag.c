#include <stdio.h>
#include <stdlib.h>

int main() {
  char buf[0x100];
  gid_t uid = geteuid();
  setresuid(uid, uid, uid);
  int fd = open("/flag.txt", 0);
  read(fd, buf, 0x100);
  puts(buf);
}
