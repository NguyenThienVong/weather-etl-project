import requests
from pathlib import Path
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = 'https://api.openweathermap.org/data/2.5/weather'

params = {
    'q': 'Ho Chi Minh City,VN',
    'units': 'metric',
    'appid': API_KEY
}
def extract_weather_data(url:str, params: dict) ->dict:

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None
    
    except ValueError as e:
        logging.error(f"Invalid JSON response: {e}")
        return None

    if not data:
        logging.warning("No data")
        return []

    output_path = "data/weather_data.json"
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True,exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data,f,indent=4)

    logging.info(f"{output_path}")

    return data


