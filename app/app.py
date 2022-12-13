import requests
from bs4 import BeautifulSoup


TARGET_URL = "https://upl.uz"


def get_and_convert_soup(url: str):
    return BeautifulSoup(requests.get(url).text, "html.parser")

def parse_category_page(page: BeautifulSoup) -> list:
    news_links = page.select("#dle-content .short-story h2.sh-tit a")
    news = []
    for new_obj in news_links:
        news.append({"name": new_obj.text, "link": new_obj["href"]})
    return news

def text_parser(page: BeautifulSoup)-> list:
    new_text = page.select("#dle-content .full-story .fstory ")
    texts = []
    for text_obj in new_text:
        texts.append({"text": text_obj.text})
    return texts

def parse_categories(page: BeautifulSoup) -> dict:
    category_links = enumerate(
        page.select(" .nav-row ul li a"),
        start=1
    )
    categories = {}
    for index, category_obj in category_links:
        categories[index] = {"name": category_obj.text, "link": category_obj["href"]}
    return categories

def text_from_dict(source_dict: dict) -> str:
    return '\n'.join(map(
        lambda command: f"\t{command[0]}: {command[1]}",
        source_dict.items()
    ))


def validate_command(command: str, command_len: int = 1) -> bool:
    return command.isdigit() and len(command) <= command_len


def check_command(command_dict: dict, user_command) -> bool:
    return command_dict.get(int(user_command), False)

def run():
    commands = {
        1: "Главная новость дня",
        2: "Новости дня по категориям"
    }
    subcommand_text = text_from_dict(commands)
    user_command = input(f"Введите номер команды\n{subcommand_text}\nВвод: ")
    if not validate_command(user_command):
        print("Попробуй заново")
        run()
    if not check_command(commands, user_command):
        print("Такой команды нет")
        run()
    user_command = int(user_command)
    main_page = get_and_convert_soup(TARGET_URL)

    if user_command == 1:
        main_new = main_page.select("#container #mainleft .topblok .topblokl a")
        main_new_text = text_parser(get_and_convert_soup(main_new[0].get("href")))
        print(text_from_dict(main_new_text[0]).splitlines())

    elif user_command == 2:
        categories = parse_categories(main_page)
        text_list = []
        for key, category_dict in categories.items():
            text_list.append(f'\t{key}: {category_dict["name"]}')
        command_text = "\n".join(text_list)
        category_id = input(f"Выберите категорию :\n{command_text}\nВвод: ")
        if not validate_command(category_id, 2):
            print("Попробуй заново")
            run()
        if not check_command(categories, category_id):
            print("Такой категории нет")
            run()
        category_page = get_and_convert_soup(TARGET_URL +  categories[int(category_id)]["link"])
        news_page = parse_category_page(category_page)
        new_names = "\n".join(map(
            lambda new: f"\t{new[0]}: {new[1]['name']}",
            enumerate(news_page, start=1)
        ))
        new_id = input(f"Выберите новость \n{new_names}\nВвод:")
        if not validate_command(new_id, 2):
            print("Такой новости нет")
            run()
        new_id = int(new_id)
        if new_id > len(news_page):
            print("Такой новости нет")
            run()
        target_new_obj = news_page[new_id - 1]
        new_text = text_parser(get_and_convert_soup(target_new_obj["link"]))
        print((text_from_dict(new_text[0])).splitlines()[-1])
