import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class YandexPolygon(webdriver.Chrome):

    def trash_taker(self):
        self.find_element(
            By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[2]/span/a"
        ).click()

    def polygon_login(self, user_login: str, user_password: str):
        self.get("https://passport.yandex.ru/auth/add?retpath=https%3A%2F%2Fyandex.ru%2Fdev%2Fdisk%2Fpoligon%2F")
        time.sleep(1)
        try:
            self.find_element(
                By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]/"
                          "div/div/div/div[1]/form/div[2]/div/div[2]/span/input"
            ).send_keys(user_login)
            time.sleep(1)
            self.find_element(
                By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[4]/button"
            ).click()
            time.sleep(5)
            self.find_element(
                    By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/"
                              "div[3]/div/div/div[1]/form/div[2]/div[1]/span/input"
                ).send_keys(user_password)
            self.find_element(
                    By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/form/div[3]/button"
                ).click()
            time.sleep(5)
            self.token_taker()
        except NoSuchElementException:
            print("Неверный логин или пароль, повторите снова")
            login = input("Введите свой логин: ")
            password = input("Введите свой пароль: ")
            self.polygon_login(login, password)



    def token_taker(self) -> str:
        try:
            self.trash_taker()
        except NoSuchElementException:
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
