from prefect import task, flow
import httpx
import json

@task
def get_temp(lat: float, long: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m"
    result = httpx.get(url)
    return result

def get_humidity(lat: float, long: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m"
    result = httpx.get(url)
    return result

@flow
def get_weather(lat, long):
    get_temp(lat, long)
    get_humidity(lat, long)

if __name__ == '__main__':
    get_weather(52.52, 13.41)