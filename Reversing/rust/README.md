# Rust

**Category**: Rev **Difficulty**: Medium **Author**: NoobMaster

# Description

Rust! Enjoy :) Note: The message that produces the provided encryption is the flag.

# Distributions
- `challenge/rust`
- `challenge/output.txt` 

# Solution

After analyzing the binary, we see that it is taking input for a message and a key. It decodes the key from hex and then calls the encrypt function, providing the message and the key as arguments (and some unknown arguments, rust being rust). We can see the encrypt functions, when meeting some conditions, prints a local variable and then returns. The local variable's value is taken from another local variable (let's call it `enc_array`). Looking at the entire function, the code performs some encryption on each byte and then pushes a certain value to `enc_array`. We can reverse these encryptions and use our knowledge of the flag format (`ictf{`) to find the key. Once we find the key, we can decrypt the entire message! Solve at `challenge/solve.py`



