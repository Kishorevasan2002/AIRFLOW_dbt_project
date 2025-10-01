# 🌦️ End-to-End Weather Data Engineering Pipeline

This project implements a **complete, containerized ELT (Extract, Load, Transform) pipeline** using a modern data stack. It automatically ingests weather forecast data from an API, transforms it for analytics, and provides a platform for visualization.

---

##  Tech Stack & Architecture

- **Orchestration**: Apache Airflow  
- **Data Transformation**: dbt (Data Build Tool)  
- **Database**: PostgreSQL  
- **Data Visualization**: Apache Superset  
- **Containerization**: Docker & Docker Compose  
- **Caching Layer**: Redis (for Superset performance)

**Pipeline Flow:**

```
[Weather API]
↓
[Airflow: PythonOperator]
↓
[PostgreSQL: Raw Table]
↓
[Airflow: DockerOperator (dbt)]
↓
[PostgreSQL: Transformed Tables]
↓
[Superset: Dashboards]
```

---

## ⚙️ How It Works

The pipeline is orchestrated by the **Airflow DAG (`orch.py`)**:

1. **Extract & Load (EL)**  
   - `weather_data_ingestion` task (PythonOperator) runs `connection.py`.  
   - Fetches data from the **National Weather Service API**.  
   - Creates the `forecast_periods` table (if not exists).  
   - Loads raw JSON into PostgreSQL.  

2. **Transform (T)**  
   - `transform_data` task (DockerOperator) runs `dbt`.  
   - Spins up a temporary **dbt-postgres** container.  
   - Executes `dbt run`, transforming raw data into clean, analytics-ready models:
     - `staging.sql`
     - `wether_report.sql`
     - `daily_average.sql`

3. **Visualization**  
   - Superset connects directly to PostgreSQL.  
   - Users can build **charts & dashboards** on top of dbt models.  

---

## 📂 Project Structure

```
.
├── airflow/
│   ├── dags/
│   │   └── orch.py              # Airflow DAG (pipeline tasks)
│   └── src/
│       ├── api_request.py       # API call helper
│       └── connection.py        # Ingestion script
│
├── dbt/
│   ├── models/
│   │   ├── daily_average.sql    # Daily avg metrics
│   │   ├── staging.sql          # Initial cleaning & preparation
│   │   └── wether_report.sql    # Final reporting table
│   └── sources.yaml             # dbt sources (raw table refs)
│
├── docker/
│   └── superset_config.py       # Superset config
│
├── airflow_init.sql             # PostgreSQL init script
└── docker-compose.yaml          # Docker Compose setup
```

---

##  Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/)  

### 🔑 Configuration
Create a `.env-superset` file inside the `docker/` directory:

```env
# docker/.env-superset

SECRET_KEY='your_strong_secret_key'

# DB connection details (must match docker-compose.yaml)
DATABASE_DIALECT=postgresql
DATABASE_USER=airflow_user
DATABASE_PASSWORD=airflow_password
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_DB=superset
```

### ▶️ Running the Pipeline
Start all services:

```bash
docker-compose up -d
```

Stop all services:

```bash
docker-compose down
```

## 🌐 Accessing Services

- **Apache Airflow** → http://localhost:8080
  - Login: `airflow` / `airflow`
  - DAG: `my_test_dag`

- **Apache Superset** → http://localhost:8088
  - Login: `admin` / `admin`
  - Add datasets from dbt models to create charts.

## 📊 dbt Models

### `staging.sql`
Cleans raw data, renames columns, casts types, adjusts timestamps.

### `wether_report.sql`
Final reporting model, selecting key fields from staging.

### `daily_average.sql`
Aggregates by day to calculate average temperature & wind speed per city.

---

## 📝 Notes

- This setup is for local development & testing.
- For production deployment, update credentials, use a secure `SECRET_KEY`, and configure volumes & networking as per environment.

---

## 📌 Future Enhancements

- CI/CD integration with GitHub Actions.
- Deployment to cloud platforms (AWS/GCP/Azure).
- Real-time streaming support via Kafka.
- Automated Superset dashboard provisioning.

---
