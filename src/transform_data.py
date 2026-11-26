import pandas as pd
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).resolve().parent.parent / 'data' / 'weather_data.json'

columns_name_to_drop = [ 'weather', 'weather_icon','sys.type']

columns_names_to_rename = {
        "base": "base",
        "visibility": "visibility",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "city_id", 
        "name": "city_name",
        "cod": "code",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperature",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressure",
        "main.humidity": "humidity",
        "main.sea_level": "sea_level",
        "main.grnd_level": "grnd_level",
        "wind.speed": "wind_speed",
        "wind.deg": "wind_deg",
        "wind.gust": "wind_gust",
        "clouds.all": "clouds",                  
        "sys.id": "sys_id",                
        "sys.country": "country",                
        "sys.sunrise": "sunrise",                
        "sys.sunset": "sunset",
        # weather_id, weather_main, weather_description 
    }
columns_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

def create_dataframe(path_name:Path) -> pd.DataFrame:

    logging.info("Loading weather JSON data")
    path = path_name
    if not path.exists():
        raise FileNotFoundError(f"{path}")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info("Weather JSON loaded successfully")
    
    return df

def normalize_weather_columns(df:pd.DataFrame) -> pd.DataFrame:
    logging.info("Normalizing weather columns")
    weather_df = pd.json_normalize(df['weather'].apply(lambda x: x [0]))

    weather_df = weather_df.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, weather_df], axis=1)
    
    logging.info("Weather columns normalized")
    return df

def drop_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    logging.info(f"Dropping unnecessary columns")
    df = df.drop(columns=columns_names,errors="ignore")
    return df

def rename_columns(df: pd.DataFrame, columns_names:dict[str,str]) -> pd.DataFrame:
    logging.info(f"Renaming columns")
    df = df.rename(columns=columns_names)
    return df

def normalize_datetime_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    logging.info(f"Converting datetime columns")
    for name in columns_names:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('Asia/Ho_Chi_Minh')
    return df

def data_transformations():
    logging.info("Starting weather transformation")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_name_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info(
        f"Transformation completed. "
        f"Rows: {len(df)}, Columns: {len(df.columns)}"
    )
    return df