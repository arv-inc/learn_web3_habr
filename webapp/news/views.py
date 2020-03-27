from flask import Blueprint, render_template
from webapp.news.models import News, Weather

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
def index():
    page_title = "Новости Python"
    weather_list = Weather.query.all()
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template(
        'news/index.html', page_title=page_title, news_list=news_list,
        weather_list=weather_list
        )
