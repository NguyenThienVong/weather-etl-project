# Weather ETL Pipeline

An end-to-end data engineering project that collects current weather for Ho Chi Minh City from the OpenWeather API, transforms the response with Python and Pandas, and loads the results into PostgreSQL. Apache Airflow schedules and monitors the workflow, and Docker Compose runs Airflow, PostgreSQL, and Redis.

## Architecture

[Open the Weather ETL architecture diagram in Lucidchart](https://lucid.app/lucidchart/c9dfcf0c-0c62-4f41-88e7-f88123487cef/edit?viewport_loc=-40%2C-214%2C1400%2C938%2C0_0&invitationId=inv_7552b718-3a54-4bb5-9042-16397011eedb)

The link opens the Lucidchart diagram editor. To embed a rendered image here, replace it with a publicly accessible image URL; the provided URL is an editor link, not a direct image URL.

```text
OpenWeather API
      |
      v
Extract JSON -> Transform with Pandas -> Load into PostgreSQL
                       ^                      ^
                       |                      |
                  Airflow DAG (weather_pipeline), scheduled hourly
                       |
                Docker Compose: Airflow + PostgreSQL + Redis
```

## ETL workflow

1. **Extract:** Request current weather from OpenWeather for `Ho Chi Minh City,VN` and save the raw response to `data/weather_data.json`.
2. **Transform:** Flatten and rename fields, normalize weather attributes, and convert Unix timestamps to Ho Chi Minh City time.
3. **Load:** Append the transformed record to the PostgreSQL table `weather_data`.
4. **Orchestrate:** The Airflow DAG `weather_pipeline` runs hourly (`0 */1 * * *`). It saves the intermediate Parquet file at `data/temp_data.parquet`.

The project provides pipeline data for querying and further analysis; it does not include a BI dashboard.

## Technology

| Technology | Purpose |
| --- | --- |
| OpenWeather API | Current weather source |
| Python, Pandas | ETL logic and data transformation |
| Apache Airflow | Scheduling and monitoring |
| Docker Compose | Local service orchestration |
| PostgreSQL | Persisting processed weather data |
| Redis | Airflow Celery task broker |

## Requirements

- Docker Desktop with Docker Compose
- An OpenWeather API key
- Git (to clone the repository)

Python 3.x and the packages in `requirements.txt` are needed only if running the ETL directly on the host instead of through Docker.

## Run with Docker Compose

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd weather-etl-project
```

### 2. Configure environment variables

Create the root Compose environment file from the example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace the placeholder passwords and Fernet key. The file configures Airflow's PostgreSQL and Redis services and the Airflow admin account.

Create `config/.env` for the ETL application and Airflow DAG:

```dotenv
API_KEY=your_openweather_api_key
DB_USER=airflow
DB_PASSWORD=the_same_postgres_password_as_in_root_env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=airflow
```

Use the same database username, password, and database name as `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` in the root `.env`. `DB_HOST=postgres` is the Compose service name. Keep both `.env` files private; they are excluded from Git.

### 3. Start the services

```bash
docker compose up -d
```

Check their status:

```bash
docker compose ps
```

The Compose file uses the official Airflow image and does not define a custom build, so `--build` is not required.

### 4. Open Airflow

Go to [http://localhost:8080](http://localhost:8080). Sign in with `_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD` from the root `.env` (defaults in the example: `admin` and a placeholder password).

In the Airflow UI, find `weather_pipeline`, enable it if paused, then trigger it manually or wait for its hourly schedule. Check the task logs to monitor each step.

### 5. Query the result

PostgreSQL is available to other Compose services under hostname `postgres` on port `5432`. The Compose file does not publish the database port to the host. To query from the PostgreSQL container, run:

```bash
docker compose exec postgres psql -U airflow -d airflow -c "SELECT * FROM weather_data;"
```

Replace `airflow` if you chose a different `POSTGRES_USER` or `POSTGRES_DB`.

### Stop the services

```bash
docker compose down
```

To also remove the PostgreSQL database volume and its stored data:

```bash
docker compose down -v
```

## Run the pipeline directly (optional)

Install the Python dependencies from `requirements.txt`, create `config/.env` with `API_KEY` and the `DB_*` values above, then run:

```bash
python main.py
```

The PostgreSQL host and port must be reachable from the host if running outside Docker. The `DB_HOST=postgres` setting only resolves inside the Compose network; for a host-side run, use a host-accessible PostgreSQL address and publish the database port in Compose if needed.

## Project structure

```text
.
├── config/                 # Airflow config and local ETL environment file
├── dags/                   # Airflow DAG definition
├── data/                   # Raw JSON and intermediate Parquet data
├── docs/                   # Project documentation
├── notebooks/              # Analysis notebook
├── src/                    # Extract, transform, and load modules
├── .env.example            # Example root Docker Compose environment
├── docker-compose.yaml
├── main.py                 # Run the ETL directly
└── requirements.txt
```

## Lessons learned

- Building an end-to-end Extract, Transform, Load workflow.
- Requesting REST API data and handling JSON responses.
- Cleaning and reshaping data with Pandas.
- Connecting a Python pipeline to PostgreSQL.
- Scheduling and monitoring workflows with Apache Airflow.
- Running dependent services with Docker Compose.

## Contact

**Nguyen Thien Vong** — Aspiring Data Engineer  
GitHub: [NguyenThienVong](https://github.com/NguyenThienVong)
