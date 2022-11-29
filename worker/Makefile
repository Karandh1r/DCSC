VERSION=v1
DOCKERUSER=karandhir

build:
	docker build -f Dockerfile -t spotify-worker .
push:
	docker tag spotify-worker $(DOCKERUSER)/spotify-worker:$(VERSION)
	docker push $(DOCKERUSER)/spotify-worker:$(VERSION)
	docker tag spotify-worker $(DOCKERUSER)/spotify-worker:latest
	docker push $(DOCKERUSER)/spotify-worker:latest