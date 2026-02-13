# FraudGuard: Real-Time Fraud Detection System

![Python](https://img.shields.io/badge/Python-ML%20Engine-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Next.js](https://img.shields.io/badge/Next.js-Frontend-black)
![Supabase](https://img.shields.io/badge/Supabase-Database-emerald)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

**FraudGuard** is a full-stack, production-oriented Machine Learning system designed to detect fraudulent credit card transactions in real time.
The project demonstrates an **end-to-end MLOps workflow**, from offline model training on imbalanced financial data to a **low-latency inference API** and an interactive monitoring dashboard.

The goal is not only predictive performance, but also **architectural clarity, scalability, and operational realism**.

## 🎯 Project Goals

This project was designed to simulate a **real-world fraud detection pipeline** with the following objectives:

* Demonstrate a **complete ML lifecycle**:

  * Data exploration
  * Model training
  * Artifact serialization
  * Production inference
* Build a **low-latency, async inference backend**
* Avoid ORM overhead to highlight **raw SQL performance**
* Provide a **real-time dashboard** for analysts
* Ensure **reproducibility through containerization**

## 🏗 Architecture Overview

The system is split into **three logical layers**:

1. **Offline ML Layer (Training)**
2. **Online Inference Layer (Backend API)**
3. **Presentation Layer (Frontend Dashboard)**

```mermaid
graph TD
    subgraph "Data Science (Offline)"
        K[Kaggle Notebook] -->|Train & Export| M[Model Artifacts .pkl]
    end

    subgraph "Backend FastAPI"
        API[Inference API] -->|Load Model| M
        API -->|Raw SQL Log| DB[(Supabase PostgreSQL)]
    end

    subgraph "Frontend Next.js"
        UI[Dashboard] -->|POST /predict| API
        UI -->|GET /history| API
    end

    User((Analyst)) -->|Simulate Transaction| UI
```

### Data Flow

1. Model is trained offline in a Jupyter/Kaggle environment.
2. Serialized pipeline (`.pkl`) is stored in `/models`.
3. FastAPI loads the model at startup.
4. Incoming transactions are:

   * Validated
   * Scored
   * Logged into PostgreSQL
5. Frontend visualizes results in real time.

## 🚀 Key Features

### 1. Machine Learning Engine

**Dataset:**
[Credit Card Fraud Detection (Kaggle)](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

* 284,807 transactions
* Only **0.172% fraudulent**

#### Core Challenges

* Extreme class imbalance
* High cost of false negatives
* PCA-transformed features (limited interpretability)

#### Modeling Strategy

| Component          | Choice             | Rationale                                |
| ------------------ | ------------------ | ---------------------------------------- |
| Algorithm          | XGBoost Classifier | State-of-the-art for tabular data        |
| Imbalance Handling | SMOTE              | Synthetic oversampling of minority class |
| Scaling            | RobustScaler       | Resistant to extreme outliers            |
| Metric             | AUPRC              | Better suited for imbalanced datasets    |

#### Performance

* **AUPRC:** > 0.85
* Recall prioritized over precision to reduce fraud leakage

### 2. High-Performance Inference Backend

Built using **FastAPI** with an emphasis on **low latency** and **I/O efficiency**.

#### Key Design Decisions

**1. Asynchronous Architecture**

* Non-blocking endpoints
* Suitable for high-throughput financial workloads

**2. Raw SQL Instead of ORM**

* Uses `asyncpg` directly
* Avoids ORM abstraction overhead
* Improves query latency and predictability

**3. Strict Data Contracts**

* Input validation with Pydantic
* Prevents malformed or unexpected transaction payloads

#### Backend Responsibilities

* Load model artifacts at startup
* Validate incoming transactions
* Run inference
* Persist results in database
* Serve historical data

### 3. Interactive Analyst Dashboard

The frontend simulates a **fraud analyst interface**.

#### Features

**Transaction Simulator**

* Generates synthetic PCA-like feature vectors
* Mimics real-world transaction patterns

**Real-Time Scoring**

* Sends transactions to `/predict`
* Displays fraud probability instantly

**Historical Logs**

* Fetches past transactions from backend
* Enables retrospective analysis

## 📂 Project Structure

```text
.
├── models/                 # Serialized model pipeline (.pkl)
├── backend/
│   ├── app/
│   │   ├── core/           # Config, database, settings
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # ML inference logic
│   │   └── main.py         # FastAPI entry point
│   └── Dockerfile
├── database/
│   └── 01_init_schema.sql  # SQL schema initialization
├── frontend/               # Next.js application
├── notebooks/              # Training and EDA notebooks
└── docker-compose.yml      # Service orchestration
```

## ⚙️ Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT_ID].supabase.co:5432/postgres
```

## 🐳 Running with Docker (Recommended)

Start the backend services:

```bash
docker-compose up --build
```

Available endpoints:

* **API Docs:**
  `http://localhost:8000/docs`
* **Health Check:**
  `http://localhost:8000/health`

## 💻 Running the Frontend Locally

```bash
cd frontend
pnpm install
pnpm run dev
```

Dashboard:

```
http://localhost:3000
```

## 📊 Data Science Workflow

The training process is documented in the `notebooks/` directory.

**Source Notebook:**
[https://www.kaggle.com/code/emanuellcs/credit-card-fraud-detection-xgboost](https://www.kaggle.com/code/emanuellcs/credit-card-fraud-detection-xgboost)

### Training Pipeline

1. Load dataset and inspect class distribution
2. Perform basic EDA to validate imbalance and feature behavior
3. Split data using **stratified train/test split** to preserve fraud ratio
4. Build an `imblearn` pipeline containing:
   - `RobustScaler` for outlier-resistant scaling
   - `SMOTE` for minority class oversampling (applied only on training folds)
   - `XGBoost` classifier
5. Train the full pipeline on the training set
6. Evaluate on the untouched test set using:
   - Predicted probabilities
   - **AUPRC (Average Precision)** as the primary metric
7. Serialize the **entire pipeline** (`scaler + SMOTE + model`) into a `.pkl` artifact

## 📈 Evaluation Strategy

Fraud detection is a **highly asymmetric cost problem**:

| Error Type     | Business Impact                                |
| -------------- | ---------------------------------------------- |
| False Negative | Fraud passes undetected (high cost)            |
| False Positive | Legitimate transaction blocked (moderate cost) |

Therefore:

* **Recall** is prioritized
* **AUPRC** is the main evaluation metric
* ROC-AUC is considered secondary

## 🔐 Production Considerations (Future Work)

Potential improvements for a real-world deployment:

* Feature store integration
* Online feature aggregation
* Model versioning (MLflow)
* Canary deployments
* Drift detection
* Alerting and monitoring

## 📜 License

This project is licensed under the **Apache License 2.0**.
