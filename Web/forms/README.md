# Forms
**Category:** Web
**Difficulty:** Medium/Hard
**Author:** lodsb

## Description

Check out an early development version of our forms application!

## Distribution

- url
- forms.tar.gz (app, Dockerfile and requirements.txt with the flag removed)

## Solution

Based on https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/. There is no charset meta tag and the `fail` function overwrites `Content-Type` header to not include charset. See `solve.py` for an example solution.