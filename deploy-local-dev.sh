
#!/bin/sh
#
# You can use this script to launch Redis and minio on Kubernetes
# and forward their connections to your local computer. That means
# you can then work on your worker-server.py and rest-server.py
# on your local computer rather than pushing to Kubernetes with each change.
#
# To kill the port-forward processes us e.g. "ps augxww | grep port-forward"
# to identify the processes ids
#
kubectl create namespace spotify
kubectl config set-context --current --namespace=spotify
kubectl -n spotify apply -f redis/redis-deployment.yaml
kubectl -n spotify apply -f redis/redis-service.yaml
kubectl -n spotify apply -f rest/rest-deployment.yaml
kubectl -n spotify apply -f rest/rest-service.yaml
kubectl -n spotify apply -f logs/logs-deployment.yaml
kubectl -n spotify apply -f worker/worker-deployment.yaml
kubectl -n spotify apply -f rest/rest-ingress.yaml

kubectl -n spotify apply -f mysql/mysql-pv.yaml
kubectl -n spotify apply -f mysql/mysql-pvc.yaml
kubectl -n spotify apply -f mysql/mysql-deployment.yaml
kubectl -n spotify apply -f mysql/mysql-service.yaml

kubectl port-forward --address 0.0.0.0 service/redis 6379:6379 &
kubectl port-forward --address 0.0.0.0 service/mysql 3306:3306 &
kubectl port-forward --address 0.0.0.0 service/rest-svc 80:80 &