FROM ubuntu:22.04

RUN /usr/sbin/useradd --no-create-home -u 1000 user

RUN DEBIAN_FRONTEND=noninteractive apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install ncat python3 apt-transport-https curl gnupg
RUN curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
RUN mv bazel-archive-keyring.gpg /usr/share/keyrings
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list
RUN DEBIAN_FRONTEND=noninteractive apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install bazel

WORKDIR /app

COPY .bazelignore /app
COPY .npmrc /app
COPY BUILD /app
COPY chall.py /app
COPY defs.bzl /app
COPY flag.txt /app
COPY hello.js /app
COPY MODULE.bazel /app
COPY MODULE.bazel.lock /app
COPY package.json /app
COPY pnpm-lock.yaml /app
COPY WORKSPACE /app
COPY wrapper.sh /app

RUN chmod 555 /app/*

RUN mkdir -p /home/user/.cache/bazel/
RUN chmod -R 777 /home/user/.cache/bazel/

USER 1000:1000

VOLUME /home

CMD ncat -klvp 1337 -m 999999 -e ./wrapper.sh
