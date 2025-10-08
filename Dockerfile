FROM node:24-bookworm


RUN apt update
RUN apt-get install -y python3-venv

COPY . /stardb
WORKDIR /stardb
RUN python3 -m venv env
RUN env/bin/pip install -r requirements.txt
RUN npm install --legacy-peer-deps
RUN npm run build

CMD ["sh", "-c", "ORIGIN=https://stardb.cu-bic.ca node build"]
