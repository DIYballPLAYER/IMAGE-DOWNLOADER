import requests
from bs4 import BeautifulSoup

from project.app.config import SEARCH_URL, YANDEX_URL


def convert_to_soup(content: str) -> BeautifulSoup:
    return BeautifulSoup(requests.get(SEARCH_URL + content).text, "html.parser")


def image_link_parser(page: BeautifulSoup) -> list:
    links = page.select(".container-fluid .row .col-md-9 .tz-gallery .row .col-sm-4 a img")
    links_container = []
    for link in links:
        link_ = link.get("data-src")
        if link_ is not None:
            links_container.append(link_)
    return links_container if links_container is not None else print(' Фoтo не найдено:(')


def image_uploader(url: str, token: str, theme: str) -> None:
    response = requests.post(YANDEX_URL,
                             headers={"Authorization": f"OAuth {token}"},
                             params={"url": f"{url}",
                                     "path": f"/{theme}.jpg"})

