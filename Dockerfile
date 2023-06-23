FROM ubuntu:latest
LABEL authors="ofcer"

ENTRYPOINT ["top", "-b"]