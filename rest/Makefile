VERSION=v1
DOCKERUSER=karandhir

build:
	docker build -f Dockerfile-rest -t spotify-rest .

push:
	docker tag spotify-rest $(DOCKERUSER)/spotify-rest:$(VERSION)
	docker push $(DOCKERUSER)/spotify-rest:$(VERSION)
	docker tag spotify-rest $(DOCKERUSER)/spotify-rest:latest
	docker push $(DOCKERUSER)/spotify-rest:latest