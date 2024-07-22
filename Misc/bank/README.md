# Bank

**Category**: Blockchain **Difficulty**: Easy **Author**: NoobMaster

# Description

Can you steal the bank's money?

# Distributions 

- `challenge/Bank.sol`
- Remote connection (challenge already hosted: `nc 34.42.229.254 40000`)

# Solution

You can see that the only way to get money is through loan or withdraw. The withdraw has strong checks making sure you cannot withdraw what you don't have. The loan function here is vulnereable. It uses an uint48, meaning the max value that variable can hold is `2**48-1`. If we take a loan for `2**48`, we get an overflow error. We can take a loan for `2**48-1`. Now, if we take a loan for 1, the variable will overflow and be 0 again! We recieved the money and the loaned is also zero! Now just deposit the required amount and get the flag. Solve at `challenge/solve.py`

