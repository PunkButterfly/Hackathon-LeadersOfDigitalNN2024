ARG DOCKERHUB_LOGIN
ARG DOCKER_BACKEND_PREIMAGE_NAME

FROM $DOCKERHUB_LOGIN/$DOCKER_BACKEND_PREIMAGE_NAME:latest

WORKDIR container/

COPY . .

CMD python api.py