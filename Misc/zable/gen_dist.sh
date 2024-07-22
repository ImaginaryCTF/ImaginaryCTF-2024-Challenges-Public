#!/bin/sh

cd challenge
export FLAG="`cat flag.txt`"
echo "jctf{not_a_real_flag}" > flag.txt
zip ../zable.dist.zip \
  .bazelignore \
  .npmrc \
  BUILD \
  chall.py \
  defs.bzl \
  docker-compose.yml \
  Dockerfile \
  flag.txt \
  hello.js \
  MODULE.bazel \
  MODULE.bazel.lock \
  package.json \
  pnpm-lock.yaml \
  WORKSPACE \
  wrapper.sh
echo ${FLAG} > flag.txt