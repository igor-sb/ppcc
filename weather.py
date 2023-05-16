import httpx  # requests capability, but can work with async
from prefect import flow, task


@task
def fetch_temperature(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    return most_recent_temp

@task
def fetch_windspeed(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="windspeed_10m"),
    )
    most_recent_windspeed = float(weather.json()["hourly"]["windspeed_10m"][0])
    return most_recent_windspeed

@task
def save_weather(temp: float):
    with open("weather.csv", "a+") as w:
        w.write(str(temp), "\n")
    return "Successfully wrote temp"


@flow
def pipeline(lat: float, lon: float):
    temp = fetch_temperature(lat, lon)
    wind = fetch_windspeed(lat, lon)
    result = save_weather(temp)
    result = save_weather(wind)
    return result


if __name__ == "__main__":
    pipeline(38.9, -77.0)