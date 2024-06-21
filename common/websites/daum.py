import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException


class Daum:
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
        c_cards = self.driver.find_elements(By.TAG_NAME, "c-card")

        for c_card in c_cards:
            try:
                c_frag = c_card.find_element(By.TAG_NAME, "c-frag")

                if c_frag.text == self.website_url:
                    c_doc_web = c_card.find_element(By.TAG_NAME, "c-doc-web")
                    a = c_doc_web.find_element(By.TAG_NAME, "a")

                    return a
            except NoSuchElementException:
                pass

    def search(self, query, start_page=1, end_page=11):
        """
        검색을 통해 블로그 게시물 탐색

        :param query: 검색어
        :param start_page: 탐색 시작 페이지
        :param end_page: 탐색 종료 페이지
        :return: 블로그 게시물 HTML 요소 || None
        """
        for current_page in range(start_page, end_page + 1):
            url = f"https://search.daum.net/search?w=fusion&col=blog&q={query}&DA=TWA&p={current_page}"

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

        # 블로그 게시물 열기 및 활성 탭 변경 후 2초 대기
        element.click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(3)

        # 스크롤 내리기
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.END)
        time.sleep(2)

        # 블로그 게시물 탭 닫기 및 활성 탭 변경 후 0.25초 대기
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(0.25)
