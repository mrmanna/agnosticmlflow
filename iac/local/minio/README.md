## Create a TLS Secret
```
kubectl create secret tls minio-tls-secret --cert=minio.crt --key=minio.key
```
## Deploy MinIO
```
kubectl apply -f minio-deployment.yaml 
kubectl apply -f minio-service.yaml
```
## Deploy Ingress
```
minikube addons enable ingress
kubectl apply -f minio-ingress.yaml
```