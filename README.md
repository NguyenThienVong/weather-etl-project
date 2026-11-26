Weather ETL Pipeline

An end-to-end Data Engineering project that extracts real-time weather data from the OpenWeather API, transforms raw JSON data using Python and Pandas, and loads structured records into PostgreSQL.

The pipeline is orchestrated by Apache Airflow and deployed using Docker Compose, with Redis serving as the Celery task broker.

---

1. Overview

Project Description

This project demonstrates the development of an automated ETL pipeline that collects current weather information for Ho Chi Minh City, Vietnam.

The pipeline follows the Extract, Transform, and Load (ETL) process:

- Extract: Retrieve current weather data from the OpenWeather API.
- Transform: Clean, flatten, normalize, and restructure raw JSON data using Python and Pandas.
- Load: Append processed weather records into a PostgreSQL database.
- Orchestration: Schedule and monitor the ETL workflow using Apache Airflow.

Project Objectives

- Build an end-to-end ETL pipeline using Python.
- Integrate external REST APIs as a data source.
- Process JSON data and convert it into structured datasets.
- Store processed data in PostgreSQL.
- Automate ETL execution using Apache Airflow.
- Containerize the application and supporting services using Docker Compose.

---

2. Data Visualization

This project focuses on data ingestion, transformation, orchestration, and storage rather than dashboard development.

The processed weather data is stored in PostgreSQL and can be queried for further analysis and visualization.

Data Output:
- Raw weather data: JSON
- Intermediate data: Parquet
- Processed data: PostgreSQL

Note: A BI dashboard is not included in the current project scope.

---

3. Data Architecture

Architecture Diagram

[Open the Weather ETL architecture diagram in Lucidchart](https://lucid.app/lucidchart/c9dfcf0c-0c62-4f41-88e7-f88123487cef/edit?viewport_loc=-40%2C-214%2C1400%2C938%2C0_0&invitationId=inv_7552b718-3a54-4bb5-9042-16397011eedb)
<img width="1138" height="516" alt="image" src="https://github.com/user-attachments/assets/cd870e56-b3c5-4fe1-bd9e-02a5f9d23d49" />

Technology Stack

| Technology | Purpose |
|---|---|
| OpenWeather API | External weather data source |
| Python | ETL implementation |
| Pandas | Data cleaning and transformation |
| Apache Airflow 3.1.7 | Workflow orchestration and scheduling |
| Docker Compose | Containerization and service management |
| PostgreSQL 16 | Relational database for processed data |
| Redis 7.2 | Celery message broker |
| Parquet | Intermediate data storage format |

ETL Workflow

Step 1: Extract

- Send HTTP requests to the OpenWeather API.
- Retrieve current weather information for Ho Chi Minh City.
- Handle API responses and HTTP errors.
- Save raw JSON data to `data/weather_data.json`.

Step 2: Transform

- Read and process raw JSON data using Python and Pandas.
- Flatten nested JSON structures.
- Rename and normalize weather attributes.
- Convert Unix timestamps into Ho Chi Minh City local time.
- Save intermediate data in Parquet format at `data/temp_data.parquet`.

Step 3: Load

- Connect to PostgreSQL using the configured database connection.
- Read transformed data.
- Append processed records to the `weather_data` table.

Step 4: Orchestration

Apache Airflow manages and schedules the ETL workflow through the `weather_pipeline` DAG.

- DAG ID: `weather_pipeline`
- Schedule: Hourly (`0 */1 * * *`)
- Catchup: Disabled

Infrastructure Architecture

Docker Compose manages the services required by the pipeline:

- Airflow: Workflow scheduling and execution.
- PostgreSQL: Database storage and Airflow metadata database.
- Redis: Message broker for CeleryExecutor.

The services communicate through the Docker Compose network.

---

4. Prerequisites

Make sure the following tools and accounts are available:

- Docker Desktop
- Docker Compose
- Git
- OpenWeather API account and API key

For running the ETL application directly on the host machine:

- Python 3.x
- Dependencies listed in `requirements.txt`

---

5. How to Run This Project

Step 1: Clone the Repository

```bash
git clone https://github.com/NguyenThienVong/weather-etl-project.git

cd weather-etl-project
```

Step 2: Configure Environment Variables

Create the root `.env` file from the example:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux / macOS:

```bash
cp .env.example .env
```

Edit the root `.env` file and replace all placeholder values, including:

- PostgreSQL credentials
- Redis password
- Airflow administrator credentials
- Airflow Fernet key

Next, create `config/.env` for the ETL application:

```env
API_KEY=your_openweather_api_key

DB_USER=airflow
DB_PASSWORD=your_postgres_password
DB_HOST=postgres
DB_PORT=5432
DB_NAME=airflow
```

Make sure the database credentials match the PostgreSQL settings in the root `.env` file.

Important: Never commit your actual `.env` files or API keys to GitHub.

Step 3: Start Docker Services

Run the following command:

```bash
docker compose up -d
```

Check the status of the containers:

```bash
docker compose ps
```

Wait until the required services become healthy.

Step 4: Access Apache Airflow

Open the Airflow web interface:

[http://localhost:8080](http://localhost:8080)

Log in using the administrator username and password configured in the root `.env` file.

Step 5: Trigger the ETL Pipeline

1. Locate the `weather_pipeline` DAG.
2. Enable the DAG if it is paused.
3. Trigger the DAG manually or wait for its hourly schedule.
4. Monitor task execution and logs through the Airflow interface.

Step 6: Verify Data in PostgreSQL

Run the following command to query the processed weather records:

```bash
docker compose exec postgres psql -U airflow -d airflow -c "SELECT * FROM weather_data;"
```

You should see the weather records stored in the `weather_data` table.

Stop the Services

To stop the containers:

```bash
docker compose down
```

To remove containers and the PostgreSQL data volume:

```bash
docker compose down -v
```

Warning: The `-v` option deletes the persisted PostgreSQL data.

---

6. Project Structure

```text
weather-etl-project/
│
├── config/
│   ├── .env
│   └── airflow.cfg
│
├── dags/
│   └── weather_pipeline.py
│
├── data/
│   ├── weather_data.json
│   └── temp_data.parquet
│
├── docs/
│   └── architecture.png
│
├── notebooks/
│   └── analysis_data.ipynb
│
├── src/
│   ├── extract_data.py
│   ├── transform_data.py
│   └── load_data.py
│
├── .env.example
├── .gitignore
├── docker-compose.yaml
├── main.py
└── requirements.txt
```

---

7. Lessons Learned

Through this project, I gained hands-on experience in:

- Building an end-to-end ETL pipeline with Python.
- Extracting data from REST APIs and handling JSON responses.
- Transforming nested JSON data using Pandas.
- Working with Parquet as an intermediate data storage format.
- Loading structured data into PostgreSQL.
- Orchestrating and scheduling workflows with Apache Airflow.
- Understanding CeleryExecutor and Redis in Airflow.
- Deploying and managing multiple services using Docker Compose.
- Managing environment variables and database connections across containers.

---

8. Contact

Nguyen Thien Vong

Aspiring Data Engineer

- GitHub: [NguyenThienVong](https://github.com/NguyenThienVong)
- Repository: [Weather ETL Pipeline](https://github.com/NguyenThienVong/weather-etl-project)

