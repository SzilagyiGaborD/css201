import pytest
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

HTML_FILE = "index.html"  # Cseréld ki a saját HTML fájlodra


@pytest.fixture
def html_content():
    """Beolvassa a HTML fájlt és BeautifulSoup objektummá alakítja."""
    with open(HTML_FILE, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")


def test_name_inside_div(html_content):
    """Ellenőrzi, hogy a név egy div elemben van-e."""
    divs = html_content.find_all("div")
    assert any("Nagy János" in div.text for div in divs), "A név nincs div elemben!"


@pytest.fixture(scope="module")
def browser():
    """Inicializálja a Selenium WebDriver-t."""
    options = Options()
    options.add_argument("--headless")
    service = Service("chromedriver")  # Cseréld ki a megfelelő WebDriver elérési útra
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{HTML_FILE}")
    yield driver
    driver.quit()


def test_box_styles(browser):
    """Ellenőrzi a doboz CSS stílusait."""
    div = browser.find_element(By.TAG_NAME, "div")
    style = div.value_of_css_property

    assert style("border-style") == "solid", "A szegély nem solid!"
    assert style("border-width") == "3px", "A szegély nem 3px!"
    assert style("border-color") == "rgba(128, 0, 128, 1)", "A szegély színe nem #800080!"
    assert style("padding") == "17px", "A belső margó nem 17px!"
    assert style("margin") == "10%", "A külső margó nem 10%!"


if __name__ == "__main__":
    pytest.main()
