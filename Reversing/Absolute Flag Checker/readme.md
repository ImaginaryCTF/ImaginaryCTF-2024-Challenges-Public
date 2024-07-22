# Absolute Flag Checker
**Category:** Rev
**Difficulty:** Medium-Hard
**Author:** Minerva.

## Description
What's easier way than verifying flag contents more times than required?

## Distribution

- `togive/absolute flag checker.exe`

## Solution
The hardcoded condition checks are a system of linear equations, made without using arrays/vectors to make reversing annoying. The linear equation is of the form AX=B, where X is the flag vector. Using linear algebra, find X by using X = (A^-1)B.
