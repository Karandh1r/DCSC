
FROM ubuntu:20.04

RUN	DEBIAN_FRONTEND=noninteractive apt-get update -y && \
	apt-get install -yq --no-install-recommends \
	   git python3 python3-pip curl

RUN  pip3 install --upgrade redis mysql-connector-python spotipy jsonpickle flask

RUN mkdir -p /tmp/output

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8


COPY worker-server.py ./

ENTRYPOINT	["python3", "./worker-server.py"]