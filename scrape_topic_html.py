"""
A scraper to collect course html from Udemy Python courses.
This is intended to show a method of collection as an example of web automation use
"""
from pathlib import Path
import time
from random import uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import undetected_chromedriver as uc
from bs4 import BeautifulSoup

from file_utils import write_text_file
from settings import (UDEMY_BASE_URL,
                      TEMP_FILES,
                      COOKIE_XPATH,
                      NEXT_PAGE_XPATH,
                      PAGE_NUM_CLASS,
                      PAGE_LIMIT)


def get_driver() -> uc.Chrome:
    """ Initialize a Chrome driver with undetected_chromedriver. """
    return uc.Chrome()


def handle_cookies(driver: uc.Chrome) -> None:
    """ Accept cookies by clicking on the relevant button. """
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, COOKIE_XPATH)))
    driver.find_element(By.XPATH, COOKIE_XPATH).click()


def load_url(driver: uc.Chrome, url: str) -> None:
    """ Load the specified URL in the given webdriver. """
    driver.get(url)
    time.sleep(uniform(0, 2))


def get_num_pages(soup: BeautifulSoup) -> int:
    """ Get the last page number """
    num = soup.find('span', class_=PAGE_NUM_CLASS)
    return int(num.text) if num else 0


def navigate_to_next_page(driver: uc.Chrome) -> None:
    """ Navigate the driver to the next page. """
    try:
        driver.find_element(By.XPATH, NEXT_PAGE_XPATH).click()
    except NoSuchElementException:
        print("Reached the last page, unable to find the next page button.")


def crawl_main_page(url: str) -> uc.Chrome:
    """ Browse the main URL and ensures correct access. """
    driver = get_driver()
    load_url(driver, url)
    handle_cookies(driver)
    time.sleep(1 + uniform(0, 3))
    return driver


def main(topic: str = 'python', page_limit: int = PAGE_LIMIT) -> None:
    """ Fetch the front page content from the course list
        and insert the output into a local file.
    """
    topic_url = f'{UDEMY_BASE_URL}/topic/{topic}'
    driver = crawl_main_page(topic_url)

    for page in range(1, page_limit + 1):
        html_path = Path.joinpath(TEMP_FILES, f'main_topic_list_page_{page}.html')
        write_text_file(html_path, driver.page_source)
        navigate_to_next_page(driver)


if __name__ == '__main__':
    main()
