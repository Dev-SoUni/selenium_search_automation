import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException


class Google:
    driver = None
    website_url = None

    def __init__(self, driver, website_url):
        self.driver = driver
        self.website_url = website_url

    def find_element(self):
        """
        블로그 게시물 HTML 요소를 탐색 후 반환

        :return: 블로그 게시물 HTML 요소 || None
        """
        body = self.driver.find_element(By.TAG_NAME, "body")

        cites = body.find_elements(By.TAG_NAME, "cite")
        for cite in cites:
            try:
                if self.website_url in cite.text:
                    return cite.find_element(By.XPATH, "ancestor::a")
            except NoSuchElementException:
                pass

        return None

    def search(self, query):
        """
        검색을 통해 블로그 게시물 탐색

        :param query: 검색어
        :return: 블로그 게시물 HTML 요소 || None
        """
        url = f"https://www.google.com/search?q={query}"

        self.driver.get(url)
        time.sleep(0.25)

        element = self.find_element()
        if element:
            return element

        return None

    def visit(self, element):
        """
        블로그 게시물 방문

        :param element: 블로그 게시물 HTML 요소
        """

        # 해당 페이지 접근
        element.send_keys(Keys.ENTER)
        time.sleep(3)

        # 스크롤 내리기
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.END)
        time.sleep(2)

        # 뒤로가기
        self.driver.back()
        time.sleep(1)
