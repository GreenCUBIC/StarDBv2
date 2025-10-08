FROM node:24-bookworm


RUN apt update
RUN apt-get install -y python3-venv

COPY . /stardb
WORKDIR /stardb
RUN python3 -m venv env
RUN env/bin/pip install -r requirements.txt
RUN npm install --legacy-peer-deps
RUN npm run build

CMD ["sh", "-c", "PROTOCOL_HEADER=x-forwarded-proto HOST_HEADER=x-forwarded-host node build"]