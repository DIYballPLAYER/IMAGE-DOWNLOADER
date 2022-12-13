import time
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


BASE_DIR = Path(__file__).resolve().parent
DRIVERS_PATH = BASE_DIR / "drivers"
DRIVERS = {
    "gecko": DRIVERS_PATH / "geckodriver.exe",
    "chrome": DRIVERS_PATH / "chromedriver.exe"
}
IMAGE_WEBSITE_LINK = "https://backiee.com/"
SEARCH_URL = "https://backiee.com/search/"
YANDEX_URL = "https://cloud-api.yandex.net/v1/disk/resources/upload"

class YandexDisk(webdriver.Chrome):

    def __init__(self, driver_path: str) -> None:
        super().__init__(executable_path=driver_path)
        self.run()

    def YandexDiskLogin(self,user_login:str, user_password:str) -> None:
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

    def PolygonLoginAndTokenTaker(self,user_login:str, user_password:str) -> str:
        self.get("https://passport.yandex.ru/auth/add?retpath=https%3A%2F%2Fyandex.ru%2Fdev%2Fdisk%2Fpoligon%2F")
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
        time.sleep(1)
        self.find_element(
            By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div[1]/form/div[3]/button"
        ).click()
        time.sleep(5)
        token_link = self.find_element(
            By.XPATH, "/html/body/div[3]/div/div/span/section/div[1]/div[1]/"
                      "div/section/div/div/section/div/div/div/div[1]/div/section/"
                      "div/div/div/div[4]/section/div/div/iframe").get_attribute('src')
        time.sleep(5)
        self.get(token_link)
        time.sleep(2)
        self.find_element(By.XPATH, "/html/body/div/section/div[1]/div/a").click()
        time.sleep(5)
        self.switch_to.frame(self.find_element(By.XPATH,
            "/html/body/div[3]/div/div/span/section/div[1]/div[1]/div/section/div/div/section/"
            "div/div/div/div[1]/div/section/div/div/div/div[4]/section/div/div/iframe"))
        token = self.find_element(By.XPATH, "/html/body/div/section/div[1]/span/input").get_attribute('value')
        print(f"Ваш токен получен: {token}")
        return token

    def ImageUploader(self, url: str, token: str, theme: str) -> None:
        self.url = url
        self.token = token
        response = requests.post(YANDEX_URL,
            headers={
            "Authorization": f"OAuth {token}"},
            params={
            "url": f"{url}",
            "path": f"/{theme}.jpg"})



    def ImageParser(self, photo_theme: str) -> None:
        self.get(IMAGE_WEBSITE_LINK)
        self.find_element(By.XPATH, "/html/body/nav/div/div/input").send_keys(photo_theme)
        time.sleep(1)
        self.find_element(By.XPATH, "/html/body/nav/div/div/button/i").click()

    def ConvertToSoup(self, content: str) -> BeautifulSoup:
        return BeautifulSoup(requests.get(SEARCH_URL + content).text, "html.parser")

    def ImageLinkParser(self, page: BeautifulSoup):
        self.page = page
        links = page.select(".container-fluid .row .col-md-9 .tz-gallery .row .col-sm-4 a img")
        links_container = []
        for link in links:
            link_ = link.get("data-src")
            if link_ is not None:
                links_container.append(link_)
        return links_container

    def close_and_quit(self) -> None:
        self.close()
        self.quit()

    def run(self) -> None:
        print("Браузер открыт")
        time.sleep(1)
        user_login = input("Приветстую пользователь\nВведите свой логин от Яндекс Диска: ")
        user_password = input("Введите свой пароль: ")
        token = self.PolygonLoginAndTokenTaker(user_login, user_password)
        self.get(IMAGE_WEBSITE_LINK)
        theme = input("Напишите тему фото которых хотите установить(на английском): ")
        self.ImageParser(theme)
        page = self.ConvertToSoup(theme)
        link_container = self.ImageLinkParser(page)
        print("Загружаю....")
        for link in link_container:
            self.ImageUploader(link, token, theme)
        print("Готово!")
        self.YandexDiskLogin(user_login, user_password)


    def __del__(self):
        self.close_and_quit()
        print("Браузер закрыт")

if __name__=="__main__":
    YandexDisk(str(DRIVERS["chrome"]))
