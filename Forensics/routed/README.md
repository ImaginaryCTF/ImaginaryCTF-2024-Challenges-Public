# routed
**Category:** Forensics
**Difficulty:** Easy
**Author:** Eth007

## Description

Can you dig a bit deeper?

## Distribution

- `routed.pkz`

## Solution

- Open Router1, and view the command line. Run `enable` to enter super-user mode, and run `show running-config` to show the configurations. Notice that a telnet password is set, using `password 7`, which is reversible encryption. Plug this into a site like https://packetlife.net/toolbox/type7/ to get the flag, which is the password.
