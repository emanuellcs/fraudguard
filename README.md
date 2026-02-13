# FraudGuard: Real-Time Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Next.js](https://img.shields.io/badge/Next.js-Frontend-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![XGBoost](https://img.shields.io/badge/XGBoost-ML%20Model-FF6600)
![License](https://img.shields.io/badge/License-Apache%202.0-green)

**FraudGuard** is a production-grade, full-stack Machine Learning system engineered to detect fraudulent credit card transactions in real time. It implements an end-to-end MLOps workflow, featuring offline model training on imbalanced financial data, a low-latency asynchronous inference API, and a reactive monitoring dashboard.

The system addresses critical challenges in financial ML, including extreme class imbalance (0.172% positive class), sub-millisecond latency requirements, and the interpretability of PCA-transformed features.

## 📋 Table of Contents

* [System Architecture](https://www.google.com/search?q=%23-system-architecture)
* [Technical Stack](https://www.google.com/search?q=%23-technical-stack)
* [ML Pipeline Strategy](https://www.google.com/search?q=%23-ml-pipeline-strategy)
* [Installation & Deployment](https://www.google.com/search?q=%23-installation--deployment)
* [API Reference](https://www.google.com/search?q=%23-api-reference)
* [Project Structure](https://www.google.com/search?q=%23-project-structure)
* [Roadmap](https://www.google.com/search?q=%23-roadmap)
* [License](https://www.google.com/search?q=%23-license)

## 🏗 System Architecture

FraudGuard utilizes a three-tier decoupled architecture designed for horizontal scalability and fault tolerance.

### High-Level Component View

```mermaid
graph TD
    subgraph Client_Layer [Client Layer]
        User[Risk Analyst / Automated System]
    end

    subgraph Frontend_Layer [Frontend Layer]
        UI[Next.js Dashboard]
        Stats[Real-time Visualization]
    end

    subgraph Application_Layer [Application Layer]
        API[FastAPI Gateway]
        Validator[Pydantic Validation]
        Inference[XGBoost Inference Engine]
    end

    subgraph Data_Layer [Data Layer]
        DB[(PostgreSQL 18)]
        ModelArtifact[[Serialized Model .pkl]]
    end

    User -->|HTTPS| UI
    UI -->|JSON / REST| API
    API -->|Schema Check| Validator
    Validator -->|Vector| Inference
    Inference -->|Load| ModelArtifact
    Inference -->|Risk Score| API
    API -->|Async Write| DB

```

### Transaction Processing Sequence

The following sequence illustrates the lifecycle of a single transaction prediction request.

```mermaid
sequenceDiagram
    participant C as Client (Dashboard)
    participant A as FastAPI Backend
    participant M as ML Service
    participant D as PostgreSQL

    C->>A: POST /api/v1/predict (Transaction Vector)
    activate A
    A->>A: Validate Payload (Pydantic)
    
    A->>M: Request Inference
    activate M
    M->>M: Preprocessing (RobustScaler)
    M->>M: XGBoost Prediction
    M-->>A: Return Risk Score & Class
    deactivate M

    par Async Logging
        A->>D: INSERT transaction_log
        A->>D: INSERT fraud_prediction
    and Return Response
        A-->>C: JSON Response (Risk Score)
    end
    deactivate A

```

## 🛠 Technical Stack

### Backend Services

| Component | Technology | Rationale |
| --- | --- | --- |
| **Runtime** | Python 3.11 | Performance optimizations and strict typing support. |
| **Framework** | FastAPI | Asynchronous concurrency for high-throughput inference. |
| **Server** | Uvicorn | ASGI implementation for production workloads. |
| **Database Driver** | asyncpg | High-performance, non-blocking PostgreSQL driver. |
| **Validation** | Pydantic v2 | Data validation and settings management. |

### Machine Learning

| Component | Technology | Rationale |
| --- | --- | --- |
| **Model** | XGBoost | Gradient boosting for tabular data with native imbalance handling. |
| **Oversampling** | SMOTE | Synthetic Minority Over-sampling Technique for class balance. |
| **Scaling** | Scikit-learn | `RobustScaler` to mitigate the impact of financial outliers. |
| **Serialization** | Joblib | Efficient persistence of the transformation pipeline and model. |

### Frontend

| Component | Technology | Rationale |
| --- | --- | --- |
| **Framework** | Next.js 16 | Server-Side Rendering (SSR) and optimized routing. |
| **UI Library** | React 19 | Component-based architecture. |
| **Styling** | TailwindCSS | Utility-first styling for rapid UI development. |
| **State** | React Hooks | Local state management for real-time monitoring. |

## 🤖 ML Pipeline Strategy

The model is trained on the [Kaggle Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud), containing 284,807 transactions with 28 PCA-transformed features.

### Challenge: Class Imbalance

Only **0.172%** of transactions in the dataset are fraudulent. Training on raw data yields a model that classifies all transactions as legitimate to maximize accuracy, failing to detect fraud.

### Solution Implementation

1. **Stratified Splitting:** Data is split 80/20 ensuring the fraud ratio remains consistent across train/test sets.
2. **Preprocessing:** Application of `RobustScaler` to handle outliers in the `Amount` feature.
3. **SMOTE (Synthetic Minority Over-sampling Technique):** Applied only to the training fold to synthesize new minority class instances, creating a balanced decision boundary.
4. **Metric Selection:** The model is optimized for **AUPRC (Area Under Precision-Recall Curve)** rather than ROC-AUC, as AUPRC provides a more accurate performance assessment for highly imbalanced datasets.

## 🚀 Installation & Deployment

### Option 1: Docker Compose (Recommended)

This method orchestrates the database, backend, and frontend containers automatically.

**Prerequisites:** Docker Engine 20.10+ and Docker Compose v2+.

```bash
# 1. Clone the repository
git clone <repository_url>
cd fraudguard

# 2. Build and start services
docker-compose up --build -d

# 3. Verify deployment
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs

```

### Option 2: Manual Local Development

**Prerequisites:** Python 3.11+, Node.js 18+, PostgreSQL 15+.

**1. Database Setup**

```bash
# Initialize PostgreSQL database
psql -U postgres -c "CREATE DATABASE fraudguard;"
psql -U postgres -d fraudguard -f database/01_init_schema.sql

```

**2. Backend Setup**

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
export DATABASE_URL="postgresql://user:password@localhost:5432/fraudguard"
export MODEL_PATH="../models/fraud_detection_pipeline.pkl"

# Run Server
uvicorn app.main:app --reload

```

**3. Frontend Setup**

```bash
cd frontend
pnpm install
# Ensure .env.local contains: NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
pnpm run dev

```

## 📡 API Reference

Base URL: `http://localhost:8000/api/v1`

### Predict Fraud

**POST** `/predict`

Analyzes a transaction vector and returns a fraud probability score.

**Payload:**

```json
{
  "time": 0.0,
  "amount": 150.00,
  "pca_features": {
    "V1": -1.3598,
    "V2": -0.0727,
    "V3": 2.5363,
    "...": "..." 
    // Requires V1 through V28
  }
}

```

**Response (200 OK):**

```json
{
  "transaction_id": "a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6",
  "risk_score": 0.8742,
  "is_fraud": true,
  "status": "Suspicious"
}

```

### Transaction History

**GET** `/history`

Retrieves the most recent transactions and their inference results.

**Query Parameters:**

* `limit` (int): Number of records to return (Default: 10).

### System Health

**GET** `/health`

Used for container orchestration health checks.

**Response:**

```json
{
  "status": "healthy",
  "database": "connected",
  "model": "loaded"
}

```

## 📂 Project Structure

```text
fraudguard/
├── backend/                   # FastAPI Application
│   ├── app/
│   │   ├── core/              # Config, DB connection, Pydantic models
│   │   ├── routers/           # API Endpoint definitions
│   │   └── services/          # Business logic & ML inference
│   └── Dockerfile
├── frontend/                  # Next.js Application
│   ├── components/            # React UI components (Gauge, Tables)
│   ├── lib/                   # API clients and utilities
│   └── Dockerfile
├── database/                  # SQL Schemas and migrations
├── models/                    # Serialized ML artifacts (.pkl)
├── notebooks/                 # Jupyter notebooks for training/EDA
└── docker-compose.yml         # Container orchestration config

```

## 🗺 Roadmap

* [ ] **Infrastructure:** Implement Kubernetes Helm charts for cloud-native deployment.
* [ ] **MLOps:** Integrate MLflow for model versioning and experiment tracking.
* [ ] **Data:** Implement a Feature Store (Feast) for online feature serving.
* [ ] **Monitoring:** Deploy Prometheus/Grafana stack for drift detection and system metrics.
* [ ] **Security:** Implement Role-Based Access Control (RBAC) and JWT authentication.

## 📜 License

This project is distributed under the **Apache License 2.0**. See the `LICENSE` file for more information.
