#!/bin/sh

ruby /app/app.rb &
/usr/sbin/nginx -g "daemon off;"
