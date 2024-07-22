#include"stdio.h"
#include"string.h"
#include"stdlib.h"

void displayhex(char[]);

int main()
{
	// Teh flag
	// char flag[]="ictf{elf_waifus_best_waifus_2h12lntka}";
	char flag[] =  "_{f2isfsatutflwa_nh2}__asitib1leefwcuk";
	// Create a shuffling scheme
	srand(0x123123D);
	for(int i=0;i<strlen(flag);i++)
	{
		char ch = flag[i];
		int index = rand()%strlen(flag);
		flag[i] = flag[index];
		flag[index] = ch;
	}
	// Print the mangled flag
	printf("%s\n",flag);
	// displayhex(flag);
	return 0;
}

void displayhex(char f[])
{
	for(int i=0;i<strlen(f);i++)
		printf("%2x ",f[i]);
	printf("\n");
}
