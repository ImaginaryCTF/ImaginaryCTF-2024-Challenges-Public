# Tango
**Category:** Crypto
**Difficulty:** Medium
**Author:** lodsb

## Description

Let's dance!

## Distribution

- the players should get a copy of `server.py`
- challenge instancer (is it necessary if there's no RCE in the app?)

## Solution

Perform bit-flipping to change user and command. Use the fact that crc32(x ^ y ^ z) = crc32(x) ^ crc32(y) ^ crc32(z) to forge the checksum.
