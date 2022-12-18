import time
from selenium.webdriver.common.by import By

from project.app.config import IMAGE_WEBSITE_LINK
from project.app.utils import convert_to_soup, image_link_parser, image_uploader
from project.app.yandex_polygon import YandexPolygon


class YandexDisk(YandexPolygon):

    def __init__(self, driver_path: str) -> None:
        super().__init__(executable_path=driver_path)
        self.run()


    def yandex_disk_login(self, user_login: str, user_password: str) -> None:
        self.get("https://passport.yandex.uz/auth/add?from=cloud&origin=disk_landing_web_"
                 "signin_ru&retpath=https%3A%2F%2Fdisk.yandex.uz%2Fclient%2Frecent&backpath=https%3A%2F%2Fdisk.yandex.uz")
        time.sleep(1)
        self.find_element(
            By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]/"
                      "div/div/div/div[1]/form/div[2]/div/div[2]/span/input"
        ).send_keys(user_login)
        time.sleep(1)
        self.find_element(
            By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[4]/button"
        ).click()
        time.sleep(3)
        self.find_element(
            By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/"
                      "div[3]/div/div/div[1]/form/div[2]/div[1]/span/input"
        ).send_keys(user_password)
        self.find_element(
            By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div[1]/form/div[3]/button"
        ).click()
        time.sleep(90)
        self.close_and_quit()


    def image_parser(self, photo_theme: str) -> None:
        self.get(IMAGE_WEBSITE_LINK)
        self.find_element(By.XPATH, "/html/body/nav/div/div/input").send_keys(photo_theme)
        time.sleep(1)
        self.find_element(By.XPATH, "/html/body/nav/div/div/button/i").click()

    def close_and_quit(self) -> None:
        self.close()
        self.quit()

    def run(self) -> None:
        print("Браузер открыт")
        time.sleep(1)
        user_login = input("Приветстую пользователь\nВведите свой логин от Яндекс Диска: ")
        user_password = input("Введите свой пароль: ")
        token = self.token_taker(user_login, user_password)
        self.get(IMAGE_WEBSITE_LINK)
        theme = input("Напишите тему фото которых хотите установить(на английском): ")
        self.image_parser(theme)
        page = convert_to_soup(theme)
        link_container = image_link_parser(page)
        print("Загружаю....")
        for link in link_container:
            image_uploader(link, token, theme)
        self.yandex_disk_login(user_login, user_password)

    def __del__(self):
        self.close_and_quit()
        print("Браузер закрыт")

