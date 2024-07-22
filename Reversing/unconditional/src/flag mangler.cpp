#include"stdio.h"
#include"stdlib.h"
#include"string.h"

  unsigned char flag[]="ictf{m0r3_than_1_way5_t0_c0n7r0l}";
//unsigned char flag[]="333333333333333333333333333333333";
unsigned char table1[] = {0x52, 0x64, 0x71, 0x51, 0x54, 0x76};
unsigned char table2[] = {1,3,4,2,6,5};

int iterate(int c)
{
	unsigned char ch=flag[c];
	//printf("%c\t",ch);
	static int counter1 = 0;
	static int counter2 = 0;
	// calculation part
	unsigned char res1 = ch ^ table1[counter1];
	unsigned char res2 = ((ch << 2) | (ch >> (8 - 2)));
	unsigned char res3 = ((ch >> table2[counter2]) | (ch << (8 - table2[counter2])));
	unsigned char res4 = ((ch >> 2) | (ch << (8 - 2))) ^ table1[counter1];
	// flag part
	bool f1 = c%2;
	bool ff1 = ch>0x60 && ch<0x7b;
	// The final fuckery. Don't quote me on that pls
	flag[c] = f1*(ff1*res1 + (!ff1)*res2) + (!f1)*(ff1*res3 + (!ff1)*res4);
	counter1 = (counter1 + f1)%6;
	counter2 = (counter2 + f1)%6;
	printf("%02x,",flag[c]);
	return c+1;
}

int main()
{
	// first positioned characters that are alphabets will be XORd with a number from table 1
	// first positioned characters that are not alphabets will be rotated twice to the left
	// second positioned characters that are alphabets will be rotated right with a number from table 2
	// second positioned characters that are not alphabets will be rotated twice to the right and XORd with a number from table 1
	iterate(iterate(iterate(
	iterate(iterate(iterate(
	iterate(iterate(iterate(
	iterate(iterate(iterate(
	iterate(iterate(iterate(
	iterate(iterate(iterate(
	iterate(iterate(iterate(
	iterate(iterate(iterate(
	iterate(iterate(iterate(
	iterate(iterate(iterate(
	iterate(iterate(iterate(0)))))))))))))))))))))))))))))))));
	return 0;
	//Shuffle at the end
		
}
