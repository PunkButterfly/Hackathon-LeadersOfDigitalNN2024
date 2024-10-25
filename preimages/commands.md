docker build --no-cache --progress=plain -t servicecicd-frontend-preimage:latest -f Dockerfile .

docker build --no-cache --progress=plain -t servicecicd-frontend:latest -f Dockerfile .

RUN pwd && ls