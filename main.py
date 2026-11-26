from src.extract_data import extract_weather_data
from src.load_data import load_data
from src.transform_data import data_transformations

import os
from pathlib import Path
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise ValueError("API key not found in .env")
url = 'https://api.openweathermap.org/data/2.5/weather'

params = {
    'q': 'Ho Chi Minh City,VN',
    'units': 'metric',
    'appid': API_KEY
}
table_name = 'weather_data'
def pipeline():

    try:

        logging.info("=" * 60)
        logging.info("STARTING WEATHER ETL PIPELINE")
        logging.info("=" * 60)

        # 1. EXTRACT
        logging.info("STEP 1: EXTRACT")

        extract_weather_data(
            url,
            params
        )

        # 2. TRANSFORM
        logging.info("STEP 2: TRANSFORM")

        df = data_transformations()

        logging.info(
            f"Transformed {len(df)} rows"
        )

        # 3. LOAD
        logging.info("STEP 3: LOAD")

        load_data(
            table_name,
            df
        )

        logging.info("=" * 60)
        logging.info("WEATHER ETL PIPELINE COMPLETED")
        logging.info("=" * 60)

    except Exception:

        logging.exception(
            "WEATHER ETL PIPELINE FAILED"
        )

        raise


if __name__ == "__main__":
    pipeline()