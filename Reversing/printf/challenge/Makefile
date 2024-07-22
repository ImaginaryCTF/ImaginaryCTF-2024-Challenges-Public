all:
	(head printf.c -c `echo "$(wc -c printf.c | grep -o '[0-9]*') - 1" | bc` && python3 gen.py | tr -d '\n' && cat end.c) > a.c
	gcc a.c -o printf -s
