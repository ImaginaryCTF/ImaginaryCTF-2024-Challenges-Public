# solitude
**Category:** Crypto
**Difficulty:** Easy-Medium
**Author:** Eth007

## Description

The best thinking has been done in solitude. The worst has been done in turmoil.
- Thomas A. Edison

## Distribution

- `main.py`
- nc

## Solution

This RNG is a variant of https://en.wikipedia.org/wiki/Solitaire_(cipher), which is vulnerable as it tends to repeat keystream bytes. We can exploit this by XORing together consecutive bytes in different flag encryptions and selecting the most common combinations. This can be used to recover the flag. (see solve.py)
