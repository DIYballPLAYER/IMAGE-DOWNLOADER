from app.config import DRIVERS
from app.yandex_disk import YandexDisk

if __name__ == "__main__":
    YandexDisk(str(DRIVERS["chrome"]))