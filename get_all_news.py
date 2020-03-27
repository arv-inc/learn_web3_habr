from webapp import create_app
from webapp.python_org_news import get_python_news
from webapp.weather import weather_by_city

app = create_app()
city_list = ["Norilsk,Russia", "Saint-Petersburg,Russia", "Yeisk,Russia"]
with app.app_context():
    get_python_news()
    for city in city_list:
        weather_by_city(city)
