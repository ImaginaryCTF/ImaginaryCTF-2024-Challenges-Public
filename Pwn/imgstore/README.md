# imgstore
**Category:** Pwn
**Difficulty:** Easy
**Author:** Brandy

## Description

Back to the old school.

## Distribution

- libc.so.6
- loader.
- imgstore.
- nc.

## Solution

Using FSB to bypass PIE, canary, and ASLR then overwrite local and global variable to zero to bypass value check. Then perform ret2libc to gain RCE.
