### Create a new namespace as a logical unit that can be in any cloud kuberenetes cluster
we will keep all data ingestion and processing in one namespace
```
kubectl create namespace cloud2-namespace
```



## Deploy Flink on Kubernetes
As we will run Apache Beam jobs in Flink, we will configure Flink docker to be capable to execute jobs in another docker with Apache Beam SDK.

```
$ cd iac/local/flink
$ eval $(minikube docker-env) 
$ docker build -t flink:1.13.0-with-docker .
```
once the docker is ready you can deploy Flink in Kubernetes
```shell
kubectl apply -f flink-conf.yaml 
kubectl apply -f flink-data-pvc.yaml 
kubectl apply -f flink-tmp-data-pvc.yaml 
kubectl apply -f flink-master-deployment.yaml 
kubectl apply -f flink-master-service.yaml 
kubectl apply -f flink-worker-deployment.yaml 
kubectl apply -f flink-worker-service.yaml 
kubectl apply -f flink-ingress.yaml 
```
