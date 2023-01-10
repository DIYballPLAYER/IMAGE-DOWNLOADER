import requests as requests
from bs4 import BeautifulSoup

from project.app.config import SEARCH_URL


def convert_to_soup(content: str) -> BeautifulSoup:
    return BeautifulSoup(requests.get(SEARCH_URL + content).text, "html.parser")



def image_link_parser(page: BeautifulSoup) -> list:
    links = page.select(".container-fluid .row .col-md-9 .tz-gallery .row .col-sm-4 a img")
    links_container = []
    for link in links:
        link_ = link.get("data-src")
        if link_ is not None:
            links_container.append(link_)
    print(links_container)
    return links_container


def image_uploader(token: str) -> None:
    theme = input("Напишите тему фото которых хотите установить(на английском): ")
    page = convert_to_soup(theme)
    link_container = image_link_parser(page)
    print(link_container)
    for link in link_container:
        response = requests.post("https://cloud-api.yandex.net/v1/disk/resources/upload",
                                 headers={"Authorization": f"OAuth {token}"},
                                 params={"url": f"{link}",
                                         "path": f"/{theme}.jpg"})
