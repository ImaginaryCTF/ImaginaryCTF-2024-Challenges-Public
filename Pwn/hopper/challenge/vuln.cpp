#include <iostream>
#include <vector>
#include <limits>
#include <stdlib.h>

using namespace std;

void menu() {
  cout << "1. alloc" << endl;
  cout << "2. remove" << endl;
  cout << "3. show" << endl;
  cout << "4. exit" << endl;
  cout << "choice> ";
}

void clean(vector<char*> &mem, vector<int> &sz) {
  for (int i=0; i<sz.size(); i++) {
    if (sz[i] == -1) {
      sz.erase(sz.begin() + i);
      mem.erase(mem.begin() + i);
    }
  }
}

void alloc(vector<char*> &mem, vector<int> &sz) {
  int siz;
  cout << "size> ";
  cin >> siz;
  mem.push_back((char*) malloc(siz));
  sz.push_back(siz);
  cout << "content> ";
  cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
  fgets(mem[mem.size()-1], siz, stdin);
}

void remove(vector<char*> &mem, vector<int> &sz) {
  int idx;
  printf("idx> ");
  cin >> idx;
  if (idx >= 0 && idx < mem.size()) {
    free(mem[idx]);
    sz[idx] = -1;
    cout << "memory deleted" << endl;
  }
}

void show(vector<char*> &mem, vector<int> &sz) {
  int idx;
  printf("idx> ");
  cin >> idx;
  if (idx >= 0 && idx < mem.size()) {
    cout << "data: ";
    cout << mem[idx];
  }
}

int main() {
  vector<char*> mem;
  vector<int> sz;

  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  int choice;

  cout << "welcome!" << endl;

  while (1) {
    menu();
    cin >> choice;

    switch(choice) {
      case 1:
        alloc(mem, sz);
        break;
      case 2:
        clean(mem, sz);
        remove(mem, sz);
        break;
      case 3:
        clean(mem, sz);
        show(mem, sz);
        break;
      default:
        exit(0);
    }

//    for (int i=0; i<sz.size(); i++) {
//      cout << sz[i] << " ";
//    }
//    cout << endl;

  }
}
