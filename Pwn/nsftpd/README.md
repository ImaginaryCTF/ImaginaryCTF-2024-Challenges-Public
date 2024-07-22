# nsftpd
**Category:** Pwn
**Difficulty:** Easy
**Author:** Eth007

## Description

Not Secure File Transfer Protocol Daemon
All credit to https://github.com/thinxer/ftp_project

## Distribution

- `ftpd`
- https://klodd.imaginaryctf.org/challenge/nsftpd

## Solution

There is a command injection in the LIST command (https://github.com/thinxer/ftp_project/blob/master/ftpd/ftp_session.c#L68). Create a directory called `|/getflag`, change directories into it, and run LIST to get the flag.
