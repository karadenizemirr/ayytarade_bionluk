import time
from selenium import webdriver
from rich.console import Console
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


console = Console()


def GET(url: str):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-images")
    driver = webdriver.Chrome(options=options)

    try:
        driver.set_page_load_timeout(10)
        driver.get(url)
        source = str(driver.page_source)
        driver.quit()
        return source
    except:
        driver.quit()
        return None
