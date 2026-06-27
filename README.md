# 🎙️ Enterprise Voice AI Platform

[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/) [![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/) [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/) [![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)](https://vuejs.org/) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

> ### 🔥 Try it live right now:
> **Frontend Dashboard:** [https://ca-enterprise-frontend.icymeadow-6921df90.eastus.azurecontainerapps.io](https://ca-enterprise-frontend.icymeadow-6921df90.eastus.azurecontainerapps.io)  
> **Backend API (Swagger):** [https://ca-enterprise-backend.icymeadow-6921df90.eastus.azurecontainerapps.io/docs](https://ca-enterprise-backend.icymeadow-6921df90.eastus.azurecontainerapps.io/docs)

An enterprise-grade, cloud-native voice processing platform. This microservices architecture allows users to upload raw audio, process it asynchronously, and retrieve deeply analyzed sentiment and transcription data via a lightning-fast REST API.

Built from the ground up for **Anti-Fragility, Massive Scalability, and Zero-Downtime**.

---

## 🚀 The "Aha!" Moment

Most voice analysis tools run locally, locking up your machine for minutes on end. This platform fundamentally flips the script. 

By leveraging a decoupled microservices architecture, you can shoot raw audio from a mobile app or web client into the cloud. The platform instantly queues the job, processes it using high-performance Python analytics, and serves it back through an ultra-fast Vue.js dashboard. 

**It is designed to handle 1 request or 10,000 requests without breaking a sweat.**

---

## 🏗️ Architecture

This project is built using elite Silicon Valley engineering standards:

*   **Backend:** High-performance REST API built in Python (FastAPI).
*   **Frontend:** Lightning-fast, reactive dashboard built in Vue.js (Vite + TailwindCSS).
*   **Containerization:** Fully containerized using Docker (Cross-platform Intel/ARM compatible).
*   **Orchestration:** Designed for Azure Kubernetes Service (AKS) or Azure Container Apps (ACA) for serverless zero-downtime scaling.
*   **Infrastructure:** Native bash deployment pipelines mapped for instant Azure CI/CD integration.

---

## 💻 Zero-Context Onboarding: Running it Locally

You don't need a massive cloud server to try this out. If you have Docker installed on your Mac or PC, you can run the entire enterprise stack locally in 30 seconds.

### 1. Clone & Build
```bash
git clone https://github.com/rajanshxrma/enterprise-voice-ai.git
cd enterprise-voice-ai

# Start the entire platform (Frontend + Backend) instantly
docker-compose up --build
```

### 2. Experience It
*   **The Dashboard:** Open your browser to [http://localhost:80](http://localhost:80) to interact with the sleek UI.
*   **The API Docs:** Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the automatically generated, interactive Swagger API documentation.

---

## ☁️ Cloud Deployment (Azure)

If you have an active Azure Subscription (Pay-As-You-Go), you can instantly deploy this architecture to the cloud using the included pipeline scripts.

```bash
# 1. Authenticate with your Azure account
az login

# 2. Build the cloud registry and inject the Docker images
bash deploy_phase1.sh

# 3. Spin up the raw Kubernetes (AKS) cluster in Central US
bash deploy_phase2.sh
```

---

