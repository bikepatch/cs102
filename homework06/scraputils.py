import requests
from bs4 import BeautifulSoup
from time import sleep

def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    news = parser.find('table', {'class': 'itemlist'})
    title_list = []
    for i in news.find_all('a', {'class': 'storylink'}):
        title_list.append(i.text)
    url_list = []
    for i in news.find_all('a', {'class': 'storylink'}):
        url_list.append(i['href'])
    author_list = []
    for i in news.find_all('a', {'class': 'hnuser'}):
        author_list.append(i.text)
    points_list = []
    for i in news.find_all('span', {'class': 'score'}):
        points_list.append(int(''.join(s for s in i.text if s.isdigit())))
    subs_list = []
    for i in news.find_all('td', {'class': 'subtext'}):
        temp = i.find_all('a')[-1].text
        if 'comment' in temp:
            subs_list.append(int(''.join(s for s in temp if s.isdigit())))
        else:
            subs_list.append(0)
    for i in range(len(author_list)):
        news_list.append({
            'author': author_list[i],
            'comments': subs_list[i],
            'points': points_list[i],
            'title': title_list[i],
            'url': url_list[i]})
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    link = parser.find("a", {"class": "morelink"})['href']
    return link


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        if n_pages:
            sleep(5)
    return news

