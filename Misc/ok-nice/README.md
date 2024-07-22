# ok-nice
**Category**: Misc **Difficulty**: Medium **Author**: NoobMaster

# Description
Ok nice

# Distributions
- `challenge/jail.py`
- Remote connection

# Solution

Solve script at: `challenge/solve.py`. Python treats True as 1 which we can use to our advantage. First, find the length of the flag by: `flag[True]`. This becomes `flag[1]`. `flag[True+True]` becomes `flag[2]` and so on. Keep on doing this until you get "error". The error would be index out of range. Next, once you know the length of the flag, use this payload `[True,True][ord(flag[True])]` so in this case `ord(flag[True])` is the ascii value of the second character of the flag (python indexing starts at 0). Next, `[True,True]` is an array of length 2. `[True,True][99]` will give an error (99 is the ascii value of "c"). However, an array of len 100 (indexing starts at zero) will not give an error. So you know the correct value of `100-1` == 99. So just keep on adding elements to the array and once you find the character, move on to the next one.

