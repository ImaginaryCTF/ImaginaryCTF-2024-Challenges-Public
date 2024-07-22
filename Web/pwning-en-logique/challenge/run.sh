#!/bin/sh

tmux new -d -s session
tmux send-keys -t session "swipl -l server.pl -g 'server(80)'" Enter
while [ 1 -eq 1 ]; do sleep 1; done
