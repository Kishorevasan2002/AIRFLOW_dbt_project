import psycopg2
from api_request import fetch_weather_data 
api_url = "https://api.weather.gov/gridpoints/TOP/31,80/forecast"

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="airflow_db",
            user="airflow_user",
            password="airflow_password",
            host="db",
            port="5432"
        )
        print("Connection successful")
        return conn
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# 2. Create table
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecast_periods (
            id SERIAL PRIMARY KEY,
            period_number INT,
            name VARCHAR(50),
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            is_daytime BOOLEAN,
            temperature INT,
            temperature_unit VARCHAR(5),
            wind_speed VARCHAR(20),
            wind_direction VARCHAR(5),
            short_forecast VARCHAR(100),
            detailed_forecast TEXT
        );
        """)
        conn.commit()
        print("Table created successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()

# 3. Insert forecast periods into DB
def insert_forecast_periods(conn, data):
    try:
        cursor = conn.cursor()
        periods = data["properties"]["periods"]
        
        for period in periods:
            cursor.execute("""
            INSERT INTO forecast_periods 
            (period_number, name, start_time, end_time, is_daytime, temperature, 
             temperature_unit, wind_speed, wind_direction, short_forecast, detailed_forecast)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                period["number"],
                period["name"],
                period["startTime"],
                period["endTime"],
                period["isDaytime"],
                period["temperature"],
                period["temperatureUnit"],
                period["windSpeed"],
                period["windDirection"],
                period["shortForecast"],
                period["detailedForecast"]
            ))
        
        conn.commit()
        print("Inserted forecast periods successfully")
    except Exception as e:
        print(f"An error occurred while inserting: {e}")
    finally:
        cursor.close()

# MAIN WORKFLOW
def main():
    conn = create_connection()
    if conn:
        create_table(conn)

        data = fetch_weather_data(api_url) 
        if data:
            insert_forecast_periods(conn, data)

        conn.close()
