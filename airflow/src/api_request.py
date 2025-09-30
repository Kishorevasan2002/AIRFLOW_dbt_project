import requests

#api_url = "http://api.weatherstack.com/current?access_key=afebf4ffbd0bfae0710ad6bccbe78cd6&query=NewYork"

def fetch_weather_data(url:str):
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            #print(data)
            return data
            
    except requests.exceptions.HTTPError as http_err:
        print(f"An HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred: {e}")

