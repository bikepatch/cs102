from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
from textblob import Word, TextBlob

classifier = None  # объявляем классификатор


def normalize(text: str) -> list:
    text = text.lower()  # переводим все в нижний регистр
    text.replace('-', ' ').replace('_', ' ').replace('/', ' ')  # заменяем знаки пробелами
    text = ''.join(
        [char for char in text if char in 'abcdefghijklmnopqrstuvwxyz ']
        )  # оставляем только английские буквы и пробелы
    return list(TextBlob(text).words.lemmatize())  # разделяем предложение на список лемматизированных слов


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
    news_list = get_news('https://news.ycombinator.com/', 1)
    count = 0
    for n in news_list:
        news = News(
            title=n['title'],
            author=n['author'],
            url=n['url'],
            comments=n['comments'],
            points=n['points']
        )
        in_database = False
        for row in s.query(News).all():
            if row.title == news.title and row.author == news.author:
                print('"{}" by {} is already in database'.format(row.title, row.author))
                in_database = True
                break
        if not in_database:
            s.add(news)
            count += 1
    s.commit()
    print(f'Added {count} news to database')
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    global classifier
    classifier = NaiveBayesClassifier(alpha=1)
    titles = [str(t[0]) for t in s.query(News.title).filter(News.label != None).all()]
    labels = [str(l[0]) for l in s.query(News.label).filter(News.label != None).all()]
    normalized= [] # со стертыми лишними знаками
    for title in titles:
        normalized.append(normalize(title))
    classifier.fit(normalized[:168], labels[:168])
    print('score:', classifier.score(normalized[168:], labels[168:]))
    print('label freq:', classifier.y_frequency)
    return redirect("/recommendations")


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

