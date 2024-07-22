f = open('bf.txt').read()

# Example

x=5
y=7
z=140

format_bf = f",>>{'+'*x}[<{'+'*y}>-]<[-<+>]<'-'*z[><]"

# Let's go through this:
# "," takes one byte input. ">>" Moves to the 2nd cell [0] -> [1] -> [2]
# The next part is basic multiplcation. It writes "x" (this case 5) in the current cell (2nd)
# It then moves left (1st cell) then add "y" (in this case 7), to the 1st cell
# it moves right to the second cell, then subtract 1. Note the `[]` indicate for loop. It stops when the current cell has a value of 0

# Detailed example:

# Input is "i". It looks like:

# [105,0,0]
# Move to cell and add "x":
# [105,0,5]
# 	     ^ (Current cell)

# Move left, Add "y", the move right, subtract one:
# [105,7,4]
# Repeat:
# [105,14,3]
# Repeat:
# [105,21,2]
# Repeat:
# [105,28,1]
# Repeat:
# [105,35,0]
#         ^ (Current cell value 0, breaks out of loop)

# As you can see, we did 7*5 = 35 :)

# "<[-<+>]<'-'*z[><]":
# Move to the left. Enter another loop. Subtract 1, move another left, add 1, move right.
# This is basically adding 35 to 105!
# [105,35,0]
# [106,34,0]
# [107,33,0]
# [108,32,0]
# And so on until it becomes:
# [140,0,0]
# After the loop, it moves to the 0th cell, and subtracts "z". Note that in case, I specifically made "z" 140 because that's how it checks! If we subtract z, we get 0, meaning the letter is correct, if we get anything else, it means that it is not!
# So now it is [0,0,0]
# It then does [><]. It just moves to the next cell and previous (infinite loop!), However, if our character is correct, moving back to the current cell has a value of 0, meaning the loop will break. It if is not, it will hang due to an infinite loop
# it continues for every character!
# If you notice, it is forming equations (as the description hinted!). We don't know the flag characters, so let's call "f" as the ascii value of each character.
# f + (x*y) - z = 0
# Let's find "x", "y", and "z"! If we know them, we can solve the equations!
f=f.replace('[><]','')
f=f.split(',>>')
f=''.join(f)
f=f.replace(">-]<[-<+>]<","")
f=f.split('[<')


z_array=[]
for i in f:
	z_array.append(i.count('-'))
z_array=z_array[1:]


f = open('bf.txt').read().strip()
f=f.replace('[><]','')
f=f.replace('-','')
f=f.split(',>>')
f=''.join(f)
f=f.split(">]<[<+>]<")

x_array=[]
y_array=[]
for i in f:
	x_count=0
	y_count=0
	x=True
	for j in i:
		if j == '+':
			if x:
				x_count+=1
			else:
				y_count+=1
		if j == '[':
			x = False
			continue
		if j == '<':
			continue 
	if x_count != 0:
		x_array.append(x_count)
	if y_count != 0:
		y_array.append(y_count)



# Found x,y, and z!

flag=[]
# f + (x*y) - z = 0
# f + (x*y) = z
# f = z - (x*y)
for i in range(len(x_array)):
	x=x_array[i]
	y=y_array[i]
	z=z_array[i]
	flag.append(chr(z-(x*y)))

print(''.join(flag)) # Got our flag!
