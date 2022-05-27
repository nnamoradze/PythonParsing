import requests
import sqlite3
from bs4 import BeautifulSoup
from time import sleep
from random import randint

page = 0
connection = sqlite3.connect("euro_asian_news.sqlite3")
cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS NEWS(ID INTEGER  PRIMARY KEY AUTOINCREMENT, "
    "TITLE TEXT, DESCRIPTION TEXT, AUTHOR TEXT, EDIT_TIME TEXT, NEWS_IMAGE_URL)")

while page <= 4:
    BASE_URL = "https://eurasianet.org/region/caucasus?gclid=CjwKCAjwj42UBhAAEiwACIhA" \
               "DljqL3ealvOCCXiG0lYgEfX5cNm_1D_fMpMBb8EkLteO1BcFTRY8QBoCn00QAvD_BwE&page=" + str(page)
    response = requests.get(url=BASE_URL)
    # print(response)
    full_soup = BeautifulSoup(response.text, 'html.parser')
    soup = full_soup.find('div', class_="views-view-sidebar__main")
    # print(soup.text)
    news = soup.findAll('div', class_="view__row")
    # print(news)

    for each_news in news:
        news_title = each_news.find('h2', class_="teaser__title").text
        news_description = each_news.find('div', class_="teaser__subtitle").text
        news_author = each_news.find('a', class_="author-link")
        news_date = each_news.find('span', class_="meta__date").text
        news_image_url = "https://eurasianet.org/" + each_news.find('div', class_="teaser__media").a.img.attrs.get(
            "src")

        if news_author is None:
            news_author = "unknown"
        else:
            news_author = news_author.text

        cursor.execute("INSERT INTO NEWS(TITLE,DESCRIPTION,AUTHOR,EDIT_TIME,NEWS_IMAGE_URL) VALUES (?,?,?,?,?)",
                       (news_title, news_description, news_author, news_date, news_image_url))
        connection.commit()

    page += 1
    sleep(randint(5, 10))
