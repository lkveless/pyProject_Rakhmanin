import json
import requests
from bs4 import BeautifulSoup


def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    url = "https://habr.com/ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    section_name = soup.find_all("article", class_="post")

    news_dict = {}
    for section in section_name:
        section_title = section.find("h2", class_="post__title").text.strip()
        section_url_id = section.find('a', class_="post__title_link")
        url_id = section_url_id['href']
        section_url = f'{url_id}'

        section_id = section_url.split("/")
        section_id = section_id[-2]

        news_dict[section_id] = {

            "section_title": section_title,
            "section_url": section_url,

        }

        with open("news_dict.json", "w") as file:
            json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    url = "https://habr.com/ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    section_name = soup.find_all("article", class_="post")

    fresh_news = {}
    for section in section_name:
        section_url_id = section.find('a', class_="post__title_link")
        url_id = section_url_id['href']
        section_url = f'{url_id}'

        section_id = section_url.split("/")
        section_id = section_id[-2]

        if section_id in news_dict:
            continue
        else:
            section_title = section.find("h2", class_="post__title").text.strip()

            news_dict[section_id] = {

                "section_title": section_title,
                "section_url": section_url,
            }

            fresh_news[section_id] = {

                "section_title": section_title,
                "section_url": section_url,
            }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    #get_first_news()
    check_news_update()


if __name__ == '__main__':
    main()