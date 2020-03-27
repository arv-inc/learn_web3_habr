from datetime import datetime

import requests
from webapp.db import db
from webapp.news.models import Weather
from webapp.config import WEATHER_API_KEY


def weather_by_city(city):
    weather_url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "format": "json",
        "num_of_days": 1,
        "lang": "ru"
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather = result.json()
        if 'data' in weather:
            if 'current_condition' in weather['data']:
                try:
                    weather = weather['data']['current_condition'][0]
                    save_weather(weather, city)
                except(IndexError, TypeError):
                    return False
    except(requests.RequestException, ValueError):
        print("Ошибка сети")
        return False
    return True


def save_weather(weather, city):
    weather_exists = Weather.query.filter(Weather.city == city).count()
    observation_time = datetime.strftime(datetime.strptime(weather['observation_time'], '%I:%M %p'), '%H:%M')
    temp_C = weather['temp_C']
    feels_like = weather['FeelsLikeC']
    windspeedKmph = weather['windspeedKmph']
    # print(weather_exists)
    print(f'{observation_time}, {city}:{temp_C}, {feels_like}')
    if not weather_exists:
        new_weather = Weather(
            city=city,
            observation_time=observation_time,
            temp_C=temp_C,
            feels_like=feels_like,
            windspeedKmph=windspeedKmph
            )
        db.session.add(new_weather)
        db.session.commit()
    else:
        city_weather_session = db.session.query(Weather).filter(Weather.city == city)
        city_weather_session = city_weather_session.update(
            {
                Weather.observation_time: observation_time,
                Weather.temp_C: temp_C,
                Weather.feels_like: feels_like,
                Weather.windspeedKmph: windspeedKmph
                },
            synchronize_session=False
            )
        db.session.commit()


if __name__ == "__main__":
    print(weather_by_city("Saint-Petersburg,Russia"))

    # Saint-Petersburg,Russia
