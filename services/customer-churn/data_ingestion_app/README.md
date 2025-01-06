## **Data Ingestion and Preprocessing App with Apache Beam and MinIO**  

## **Introduction**  
This application is designed to handle **data ingestion** and **preprocessing** tasks in a **scalable and distributed** manner using **Apache Beam** and **MinIO**. It processes raw sales data, applies transformations, and stores the results in a **MinIO bucket**.  

The app leverages **Apache Beam’s SparkRunner** to support distributed processing within a **Kubernetes cluster (Minikube)**, making it suitable for **multi-cloud deployments**.  

---

## **Key Highlights**  

### **Apache Beam Integration:**  
- **Distributed and Scalable Transformations:** Built with **Apache Beam** for parallel and scalable data processing.  
- **Flexible Runners:** Supports **FlinkRunner** and **SparkRunner** for cloud and local environments.  

### **Preprocessing Pipeline:**
- **Validation Checks:** Ensures data integrity by handling missing values, duplicates, and malformed data.
- **Transformations:**
  - Generates domain-specific features like purchase frequency, refund flags, and recent purchase indicators.
  - Computes derived metrics for customer behavior analysis, enabling churn prediction models.
- **Aggregation and Feature Engineering:**
Adds features like frequency of purchases, refund rates, and activity recency to capture behavioral patterns for churn modeling.

### **Kubernetes-Ready:**  
- **Dockerized Application:** Easily deployable as a **Docker container**.  
- **ConfigMaps and Secrets:** Supports dynamic configurations for cloud environments.  
- **Liveness and Readiness Probes:** Ensures fault tolerance during deployment.  

---

## **Features**  
- Downloads and preprocesses public sales data.  
- Performs data validation and transformations using **Apache Beam** and **SparkRunner**.  
- Stores both **raw** and **processed data** in MinIO buckets.  
- Scalable and ready for deployment in **multi-cloud Kubernetes clusters**.  

---


### **2. Installation:**  

**1. Clone the Repository:**  
```bash
git clone <repo-url>
cd data_ingestion_app
```

**2. Install Dependencies with Poetry:**  
```bash
poetry install
```

**3. Build Docker Image:**  
```bash
docker build -t data-ingestion-app .
```

