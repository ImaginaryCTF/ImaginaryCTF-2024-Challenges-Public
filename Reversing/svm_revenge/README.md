# SVM Revenge
**Category:** Reversing
**Difficulty:** Medium/Hard
**Author:** lodsb

## Description

As foretold, the revenge of SVM from round 46 is here!

## Distribution

- the players should get a copy of `svm_revenge` and `output.bin`

## Solution

Figure out that the VM uses a queue to perform all operations. Reverse-engineer the VM's bytecode and figure out that for each block of 16 characters it generates 16 linear equations mod 256. Solve the system of equations for each block to recover the flag.
