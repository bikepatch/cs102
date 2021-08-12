from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
from sqlalchemy.orm import load_only


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    news_id = int(request.query.id)
    news_label = str(request.query.label)
    s = session()
    s.query(News).filter_by(id=news_id).update({'label': news_label})
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    list_n = get_news('https://news.ycombinator.com/', 5)
    old = s.query(News).all()
    old_list = []
    for news in old:
        old_list.append((news.title, news.author) )
    for news in list_n:
        if (news['title'], news['author']) not in old_list:
            add = News(
                title=news['title'],
                author=news['author'],
                url=news['url'],
                comments=news['comments'],
                points=news['points'],
                label=None)
            s.add(add)
            print(news)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    classifier = NaiveBayesClassifier()
    train_news = s.query(News).filter(News.label is not None).options(load_only("title", "label")).all()
    x_train = [row.title for row in train_news]
    y_train = [row.label for row in train_news]
    classifier.fit(x_train, y_train)
    test_news = s.query(News).filter(News.label is None).all()
    x = [row.title for row in test_news]
    labels = classifier.predict(x)
    good = []
    maybe = []
    never = []
    for i in range(len(test_news)):
        if labels[i] == 'good':
            good.append(test_news[i])
        if labels[i] == 'maybe':
            maybe.append(test_news[i])
        if labels[i] == 'never':
            never.append(test_news[i])

    return template('recommendations_template', {'good': good, 'never': never, 'maybe': maybe})


@route('/recommendations')
def recommendations():
    global classifier
    if not classifier:
        return redirect('/classify')
    else:
        news_list = get_news('https://news.ycombinator.com/newest', 1)
        titles = [item['title'] for item in news_list]
        normal_titles = []
        for title in titles:
            normal_titles.append(normalize(title))
        labels = classifier.predict(normal_titles)
        for i in range(len(news_list)):
            news_list[i]['label'] = labels[i]
        return template('news_recommendations', rows=news_list)


if __name__ == "__main__":
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    run(host="localhost", port=8080)

