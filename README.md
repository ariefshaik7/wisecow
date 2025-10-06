# Wisecow - End to End DevOps Pipeline

This repository contains end to end DevOps immplementation of the `wisecow` application using tools like kubernetes, docker, GitHub Actions etc.

This Readme file provides instructions on how to build, run, and deploy the application using Docker and Kubernetes.

---
![argocd](/assets/images/wisecow.png)

---

## Prerequisites

Before you begin, ensure you have the following tools installed:

* **Docker**: To build and run the application container.
    
* **kubectl**: To interact with your Kubernetes cluster.
    
* **Helm**: To deploy the application to Kubernetes using the provided chart.
    
* **Cloud Provider CLI**:
    
    * **Azure CLI (**`az`) for AKS.
        
    * **AWS CLI (**`aws`) and `eksctl` for EKS.
        
    * **Google Cloud SDK (**`gcloud`) for GKE.
        
---

### Project Structure

The project is organized into the following directories and files:

* `.github/workflows/`: This directory contains the GitHub Actions workflow file (`ci-cd.yaml`) for CI/CD.
    
* [`Problem -Statement-2/`](./Problem%20-Statement-2/): This directory contains a backup script, a health check script and a system health monitor script.
    
* `argocd/`: This directory contains the Argo CD application manifest (`argocd-application.yaml`) for GitOps deployment.
    
* `cluster-setup/`: This directory contains the `selfsigned-issuer.yaml` file for setting up a self-signed certificate issuer with cert-manager.
    
* `helm/wisecow-chart/`: This is the Helm chart directory for the application.
    
    * `Chart.yaml`: Contains information about the chart.
        
    * `values.yaml`: Contains the default configuration values for the chart.
        
    * `templates/`: Contains the Kubernetes manifest templates.
        
        * `deployment.yml`: Defines the Deployment for the application.
            
        * `service.yml`: Defines the Service to expose the application.
            
        * `ingress.yml`: Defines the Ingress to expose the application to the internet.
            
* [`wisecow/`](./wisecow/): This directory contains the application source code and Dockerfile.
    
    * [`wisecow.sh`]: The main application script.
        
    * `Dockerfile`: The Dockerfile to build the application image.
        
    * [`README.md`]: The README file for the application.
        
---


## Kubernetes Deployment

The application can be deployed to any Kubernetes cluster using the provided Helm chart.

### General Deployment Steps

1. **Install NGINX Ingress Controller:**
    
    Bash
    
    ```plaintext
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace
    ```
    
2. **Install cert-manager (for TLS):**
    
    Bash
    
    ```plaintext
    helm repo add jetstack https://charts.jetstack.io
    helm repo update
    helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.12.0 --set installCRDs=true
    ```
    
3. **Apply the ClusterIssuer:**
    
    Bash
    
    ```plaintext
    kubectl apply -f cluster-setup/selfsigned-issuer.yaml
    ```
    
4. **Deploy the wisecow application:**
    
    Navigate to the `helm/wisecow-chart` directory and run:
    
    Bash
    
    ```plaintext
    helm install wisecow . --namespace wisecow --create-namespace
    ```
    

### Platform-Specific Instructions

#### Azure Kubernetes Service (AKS)

1. **Create an AKS cluster:**
    
    Bash
    
    ```plaintext
    az group create --name myResourceGroup --location eastus
    az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 1 --enable-addons monitoring --generate-ssh-keys
    ```
    
2. **Get cluster credentials:**
    
    Bash
    
    ```plaintext
    az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
    ```
    
3. **Follow the General Deployment Steps.**
    

#### Amazon Elastic Kubernetes Service (EKS)

1. **Create an EKS cluster:**
    
    Bash
    
    ```plaintext
    eksctl create cluster --name my-cluster --region us-west-2 --nodegroup-name standard-workers --node-type t3.medium --nodes 3 --nodes-min 1 --nodes-max 4 --managed
    ```
    
2. **Configure kubectl:**
    
    `eksctl` will automatically configure your `kubeconfig` file.
    
3. **Follow the General Deployment Steps.**
    

#### Google Kubernetes Engine (GKE)

1. **Create a GKE cluster:**
    
    Bash
    
    ```plaintext
    gcloud container clusters create my-gke-cluster --num-nodes=3 --zone=us-central1-c
    ```
    
2. **Get cluster credentials:**
    
    Bash
    
    ```plaintext
    gcloud container clusters get-credentials my-gke-cluster --zone=us-central1-c
    ```
    
3. **Follow the General Deployment Steps.**
    

## CI/CD with GitHub Actions

This repository includes a GitHub Actions workflow defined in `.github/workflows/ci-cd.yaml`. This workflow automates the following process:

1. **Trigger**: The workflow is triggered on every push to the `master` branch.
    
2. **Build and Push Docker Image**: It builds a new Docker image, tags it with the GitHub run ID, and pushes it to Docker Hub.
    
3. **Update Helm Chart**: It updates the `values.yaml` file in the Helm chart with the new image tag and pushes the change to the repository.
    

To use this workflow, you will need to configure the following secrets in your GitHub repository:

* `DOCKERHUB_USERNAME`: Your Docker Hub username.
    
* `DOCKERHUB_PASSWORD`: Your Docker Hub password or access token.
    
* `GIT_PAT`: A GitHub Personal Access Token with repository write access.
    

## GitOps with Argo CD

You can also deploy the `wisecow` application using a GitOps approach with Argo CD.

1. **Install Argo CD:**
    
    Bash
    
    ```plaintext
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    ```
    
2. **Apply the Argo CD Application manifest:**
    
    Bash
    
    ```plaintext
    kubectl apply -f argocd/argocd-application.yaml
    ```
    

This will create an Argo CD application that continuously monitors the `helm/wisecow-chart` directory in your Git repository and automatically deploys any changes to your Kubernetes cluster.

---
![argocd](/assets/images/argocd.png)


---

### YAML Files Explained

* `helm/wisecow-chart/templates/deployment.yml`: This file defines the Kubernetes Deployment for the `wisecow` application. It specifies the number of replicas, the container image to use, and the ports to expose.
    
* `helm/wisecow-chart/templates/service.yml`: This file defines the Kubernetes Service for the `wisecow` application. It exposes the application within the cluster so that other services can access it.
    
* `helm/wisecow-chart/templates/ingress.yml`: This file defines the Kubernetes Ingress for the `wisecow` application. It exposes the application to the internet and configures TLS termination.
    
* `cluster-setup/selfsigned-issuer.yaml`: This file defines a `ClusterIssuer` for `cert-manager`. This `ClusterIssuer` is configured to issue self-signed certificates, which is useful for development and testing.
    
* `.github/workflows/ci-cd.yaml`: This file defines the GitHub Actions workflow for CI/CD. It builds and pushes a Docker image to Docker Hub and then updates the Helm chart with the new image tag.
    
* `argocd/argocd-application.yaml`: This file defines the Argo CD Application for GitOps. It tells Argo CD to monitor the Git repository for changes and automatically deploy them to the Kubernetes cluster.
    

### Workflow and TLS/SSL

The workflow is as follows:

1. A developer pushes a change to the `master` branch of the Git repository.
    
2. The GitHub Actions workflow is triggered.
    
3. The workflow builds a new Docker image and pushes it to Docker Hub.
    
4. The workflow updates the `values.yaml` file in the Helm chart with the new image tag and pushes the change to the repository.
    
5. Argo CD detects the change in the Git repository and automatically deploys the new version of the application to the Kubernetes cluster.
    

TLS/SSL is implemented using `cert-manager`. The `Ingress` resource is annotated with [`cert-manager.io/cluster-issuer`](http://cert-manager.io/cluster-issuer)`: selfsigned-issuer`, which tells `cert-manager` to issue a certificate for the [`wisecow.local.com`](http://wisecow.local.com) hostname using the `selfsigned-issuer`. `cert-manager` then creates a `Certificate` resource and a `Secret` containing the TLS certificate and key. The Ingress controller uses this `Secret` to terminate TLS for the `wisecow` application.

---


### Running with Minikube

**1\. Start Minikube:**

Bash

```plaintext
minikube start
```

**2\. Install NGINX Ingress Controller:**

Bash

```plaintext
minikube addons enable ingress
```

**3\. Install cert-manager:**

Bash

```plaintext
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.12.0 --set installCRDs=true
```

**4\. Apply the ClusterIssuer:**

Bash

```plaintext
kubectl apply -f cluster-setup/selfsigned-issuer.yaml
```

**5\. Deploy the wisecow application:**

Bash

```plaintext
helm install wisecow helm/wisecow-chart --namespace wisecow --create-namespace
```

**6\. Add an entry to your** `/etc/hosts` file:

Bash

```plaintext
echo "$(minikube ip) wisecow.local.com" | sudo tee -a /etc/hosts
```

**7\. Access the application:**

Open your browser and navigate to [`https://wisecow.local.com`](https://wisecow.local.com).

---

### Running with Kind

**1\. Create a Kind cluster with Ingress support:**

Bash

```plaintext
kind create cluster --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF
```

**2\. Install NGINX Ingress Controller:**

Bash

```plaintext
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

**3\. Wait for the Ingress controller to be ready:**

Bash

```plaintext
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

**4\. Install cert-manager:**

Bash

```plaintext
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.12.0 --set installCRDs=true
```

**5\. Apply the ClusterIssuer:**

Bash

```plaintext
kubectl apply -f cluster-setup/selfsigned-issuer.yaml
```

**6\. Deploy the wisecow application:**

Bash

```plaintext
helm install wisecow helm/wisecow-chart --namespace wisecow --create-namespace
```

**7\. Add an entry to your** `/etc/hosts` file:

Bash

```plaintext
echo "127.0.0.1 wisecow.local.com" | sudo tee -a /etc/hosts
```

**8\. Access the application:**

Open your browser and navigate to [`https://wisecow.local.com`](https://wisecow.local.com).

---

## Running Locally with Docker

To run the application on your local machine, follow these steps:

1. **Build the Docker image:**
    
    Bash
    
    ```plaintext
    docker build -t wisecow:latest .
    ```
    
2. **Run the Docker container:**
    
    Bash
    
    ```plaintext
    docker run -p 4499:4499 wisecow:latest
    ```
    
3. **Access the application:**
    
    Open your web browser and navigate to [`http://localhost:4499`](http://localhost:4499). You should see a wise cow!
    
---
