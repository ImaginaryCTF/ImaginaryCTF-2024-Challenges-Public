#!/bin/sh

kctf_setup && \
    mount -t tmpfs none /tmp && \
    while true; do kctf_drop_privs env PLAYWRIGHT_BROWSERS_PATH=0 /usr/bin/node /home/user/bot.js; done & \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow socat STDIN TCP\:localhost\:1338"
