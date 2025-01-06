# Project Name: Apache Flink with Apache Beam on Minikube

## Overview

This project sets up and deploys **Apache Flink** with **Apache Beam** on **Minikube** for scalable data processing pipelines. It provides a fully containerized and Kubernetes-based infrastructure designed for development, testing, and prototyping workflows.

### **Core Components**

1. **Minikube Cluster** - A local Kubernetes cluster to host all components.
2. **Flink JobManager** - Manages job execution and coordinates with TaskManagers.
3. **Flink TaskManager** - Executes distributed data processing tasks as directed by the JobManager.
4. **Beam Job Server** - Accepts Apache Beam jobs and submits them to Flink for execution.
5. **Data Ingestion App** - Submits jobs to the Beam Job Server for processing data.
6. **MinIO DataLake** - Provides object storage for raw and processed data.

### **Component Interaction**

- The **Data Ingestion App** submits processing jobs to the **Beam Job Server**.
- The **Beam Job Server** delegates job execution to the **Flink JobManager**.
- The **Flink JobManager** coordinates distributed execution with **Flink TaskManagers**.
- The **Data Ingestion App** interacts with **MinIO** for raw data storage.
- The **Flink TaskManagers** interact with **MinIO** for storing processed data.



---

## **Prerequisites**

### **Tools Required**

- [Minikube](https://minikube.sigs.k8s.io/docs/start/): Kubernetes cluster manager for local setups.
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/): Kubernetes CLI for managing cluster resources.
- [Docker](https://docs.docker.com/get-docker/): Container platform for building and running containerized applications.

### **Installing Dependencies**

#### **Minikube**

1. **Install Minikube**:

   - **macOS**:
     ```sh
     brew install minikube
     ```
   - **Linux**:
     ```sh
     curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
     sudo install minikube-linux-amd64 /usr/local/bin/minikube
     ```
   - **Windows**:
     Download from [Minikube Releases](https://github.com/kubernetes/minikube/releases).

2. **Start Minikube**:

   ```sh
   minikube start
   ```

#### **kubectl**

1. **Install kubectl**:

   - **macOS**:
     ```sh
     brew install kubectl
     ```
   - **Linux**:
     ```sh
     curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
     sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
     ```
   - **Windows**:
     Download from [Kubernetes Releases](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/).

2. **Verify kubectl**:

   ```sh
   kubectl version --client
   ```

#### **Docker**

1. **Install Docker**:

   - **macOS**:
     ```sh
     brew install --cask docker
     ```
   - **Linux**:
     Follow instructions on [Docker Website](https://docs.docker.com/engine/install/).
   - **Windows**:
     Download from [Docker Website](https://docs.docker.com/docker-for-windows/install/).

2. **Start Docker Service**:

   ```sh
   sudo systemctl start docker
   ```

3. **Verify Docker Installation**:

   ```sh
   docker --version
   ```

---

## **Project Structure**

```
AGNOSCTICMLFLOW
├── documentation
│   ├── Components.png
│   ├── architecture-diagram.png
│   ├── README.md
│
├── iac                           # Infrastructure as Code (Deployment Configurations)
│   ├── cloud                     # Placeholder for Cloud Deployment Configurations
│   ├── local                     # Local Kubernetes Deployment Configurations
│   │   ├── beam                  # Apache Beam JobServer Configurations
│   │   │   ├── beam-src          # Source files or configurations for Beam
│   │   │   ├── beam-jobserver-deployment.yaml
│   │   │   ├── beam-jobserver-service.yaml
│   │   │
│   │   ├── flink                 # Apache Flink Configurations
│   │   │   ├── Dockerfile
│   │   │   ├── entrypoint.sh
│   │   │   ├── flink-conf.yaml
│   │   │   ├── flink-data-pvc.yaml
│   │   │   ├── flink-ingress.yaml
│   │   │   ├── flink-master-deployment.yaml
│   │   │   ├── flink-master-service.yaml
│   │   │   ├── flink-tmp-data-pvc.yaml
│   │   │   ├── flink-worker-deployment.yaml
│   │   │   ├── flink-worker-service.yaml
│   │   │
│   │   ├── minio                 # MinIO Object Storage Configurations
│   │   │   ├── minio-deployment.yaml
│   │   │   ├── minio-ingress.yaml
│   │   │   ├── minio-service.yaml
│   │   │   ├── minio.crt
│   │   │   ├── minio.key
│   │   │
│   │   ├── spark                 # Apache Spark Configurations
│   │   │   ├── Dockerfile-spark-standalone
│   │   │   ├── spark-ingress.yaml
│   │   │   ├── spark-master-deployment.yaml
│   │   │   ├── spark-master-service.yaml
│   │   │   ├── spark-worker-deployment.yaml
│   │   │   ├── spark-worker-service.yaml
│   │   │
│   │   ├── README.md
│
├── onprem                        # Placeholder for On-Prem Deployment Configurations
│   ├── README.md
│
├── middleware                    # Middleware Configurations (If applicable)
│   ├── README.md
│
├── portal                        # UI/Portal for Application Management
│   ├── README.md
│
├── services                      # Microservices for Specific Tasks
│   ├── customer-churn            # Domain-Specific Use Cases
│   │   ├── data_ingestion_app    # Data Ingestion Application
│   │   │   ├── scripts           # Utility Scripts for Data Handling
│   │   │   ├── src               # Source Code
│   │   │   ├── tests             # Unit and Integration Tests
│   │   │   ├── Dockerfile        # Container Configuration for App
│   │   │   ├── ingestion-deployment.yaml
│   │   │   ├── kube-config.yaml
│   │   │   ├── poetry.lock       # Dependency Lock File
│   │   │   ├── pyproject.toml    # Python Project Configuration
│   │   │   ├── README.md
│   │   │   ├── requirements.txt  # Python Dependencies
│   │   │   ├── sales_data.csv    # Example Dataset
│   │   │   ├── model_builder     # Model Training Code
│   │   │   ├── predictor         # Model Serving Code
│   │   │   ├── trainer           # Model Training Pipeline
│   │   │
│   │   ├── domain-2              # Additional Domain Services (Placeholder)
│   │   │   ├── README.md
│
├── README.md                     # Main Documentation and Instructions

```

---

## **Setup Instructions**

### **1. Start Minikube**

```sh
minikube start --cpus=4 --memory=12288 --disk-size=50g
```
### **2. Deploy Minio Data Lake**

#### Create a TLS Secret
```
kubectl create secret tls minio-tls-secret --cert=minio.crt --key=minio.key
```
#### Deploy MinIO in Default Namespace
```
kubectl apply -f minio-deployment.yaml 
kubectl apply -f minio-service.yaml
```
#### Deploy Ingress
```
minikube addons enable ingress
kubectl apply -f minio-ingress.yaml
```

### **3. Deploy Flink in Different Namespace**

#### **Create a Namespace for Flink and Others**
```
kubectl create namespace cloud2-namespace

kubectl config set-context --current --namespace=cloud2-namespace
```

#### **Build Custom Flink Docker**
```
docker build -t flink:1.13.0-with-docker .
```
#### **Deploy Flink ConfigMap and Volumes**

```sh
kubectl apply -f iac/local/flink/flink-conf.yaml
kubectl apply -f iac/local/flink/flink-data-pvc.yaml
kubectl apply -f iac/local/flink/flink-tmp-data-pvc.yaml
```
####  **Deploy Flink JobManager**
```sh
kubectl apply -f iac/local/flink/flink-master-deployment.yaml
kubectl apply -f iac/local/flink/flink-master-service.yaml
```

#### **Deploy Flink TaskManager**

```sh
kubectl apply -f iac/local/flink/flink-worker-deployment.yaml
kubectl apply -f iac/local/flink/flink-worker-service.yaml
```
#### **Deploy Flink Ingress**
```
kubectl apply -f iac/local/flink/flink-ingress.yaml
```

### 4. **Deploy Beam Job Server**

```sh
kubectl apply -f iac/local/beam/beam-jobserver-deployment.yaml
```

### 5. **Verify Deployments**

```sh
kubectl get pods -n cloud2-namespace
kubectl get svc -n cloud2-namespace
```

---

### **6. Running the Data Ingestion App**

#### **Build the Docker Image**

```sh
docker build -t data-ingestion-app:latest -f src/Dockerfile .
```

####  **Deploy the Data Ingestion App**

```sh
kubectl apply -f iac/local/data-ingestion-deployment.yaml
```

####  **Monitor Logs**

```sh
kubectl logs -f <pod-name> 
```

---

## **Key Features**

- **Scalability**: Distributed processing using Flink and Beam.
- **Data Storage**: Integrated with MinIO for scalable object storage.
- **Extensibility**: Flexible architecture to support additional pipelines.
- **Local Testing**: Minikube ensures easy local development and testing.

---

## **Troubleshooting**

### 1. Check Logs:

```sh
kubectl logs <pod-name> -n cloud2-namespace
```

### 2. Debug Kubernetes Pods:

```sh
kubectl exec -it <pod-name> -- /bin/bash
```

### 3. Check Node Resources:

```sh
kubectl describe node
```

---

## **Conclusion**

This project sets up a scalable data pipeline using Kubernetes, Flink, and Beam, providing an environment for developing distributed data processing workflows. It is ideal for prototyping and integrating with cloud-native platforms for production deployment.

For further enhancements, consider integrating monitoring tools like **Prometheus** and **Grafana** or extending workflows for multi-cloud deployments.

