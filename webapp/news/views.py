from flask import abort, Blueprint, render_template
from webapp.news.models import News, Weather

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
def index():
    page_title = "Новости Python"
    weather_list = Weather.query.all()
    news_list = News.query.order_by(News.published.desc()).all()
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.published.desc()).all()
    return render_template(
        'news/index.html', page_title=page_title, news_list=news_list,
        weather_list=weather_list
        )


@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()

    if not my_news:
        abort(404)

    return render_template('news/single_news.html', page_title=my_news.title, news=my_news)
