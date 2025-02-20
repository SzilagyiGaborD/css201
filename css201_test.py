import pytest
from bs4 import BeautifulSoup

HTML_FILE = "styled_name_box.html"  # A megfelelő HTML fájl neve

@pytest.fixture
def html_content():
    """Beolvassa a HTML fájlt és BeautifulSoup objektummá alakítja."""
    with open(HTML_FILE, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")

def test_name_inside_div(html_content):
    """Ellenőrzi, hogy a név egy div elemben van-e."""
    divs = html_content.find_all("div", class_="name-box")
    assert any("Nagy János" in div.text for div in divs), "A név nincs a megfelelő div elemben!"

def test_box_styles_inline(html_content):
    """Ellenőrzi a doboz CSS stílusait, ha inline stílus van használva."""
    div = html_content.find("div", class_="name-box")
    assert div, "A name-box osztályú div nem található!"
    
    style = div.get("style", "")
    styles = dict(s.strip().split(":") for s in style.split(";") if ":" in s)
    
    assert styles.get("border-style") == "solid", "A szegély nem solid!"
    assert styles.get("border-width") == "3px", "A szegély nem 3px!"
    assert styles.get("border-color") in ["#800080", "rgba(128, 0, 128, 1)"], "A szegély színe nem #800080!"
    assert styles.get("padding") == "17px", "A belső margó nem 17px!"
    assert styles.get("margin") == "10%", "A külső margó nem 10%!"
