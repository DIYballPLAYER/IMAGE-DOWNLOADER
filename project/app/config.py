from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DRIVERS_PATH = BASE_DIR / "Drivers"
DRIVERS = {
    "gecko": DRIVERS_PATH / "geckodriver.exe",
    "chrome": DRIVERS_PATH / "chromedriver.exe"
}
IMAGE_WEBSITE_LINK = "https://backiee.com/"
SEARCH_URL = "https://backiee.com/search/"
YANDEX_URL = "https://cloud-api.yandex.net/v1/disk/resources/upload"