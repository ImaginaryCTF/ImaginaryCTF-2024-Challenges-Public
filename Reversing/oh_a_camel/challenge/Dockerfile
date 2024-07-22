FROM ocaml/opam:debian-10-ocaml-4.13 AS builder

USER root
RUN apt update -y && apt install -y python3 python3-venv libgmp-dev pkg-config zlib1g-dev
RUN opam install cryptokit

WORKDIR /output
COPY src .
RUN chmod +x preprocess.sh
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install -U pip && pip install pycryptodome && python3 generate.py
RUN opam exec -- dune build

RUN cp _build/default/bin/main.exe .

FROM scratch AS output

WORKDIR output

COPY --from=builder /output/main.exe .