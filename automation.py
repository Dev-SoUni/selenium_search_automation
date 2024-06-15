import time
import json

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def make_url(query):
    """
    `daum` 검색 URL을 생성해줍니다.

    :param query: 검색어 키워드
    :return: 검색 키워드가 포함된 URL
    """
    return f"https://search.daum.net/search?w=tot&DA=PGD&q={query}"


def load_data():
    """
    `./data/search.json` 파일을 읽어 반환합니다.

    :return: `search.json`
    """
    file = open("./data/search.json", "r")

    json_data = json.load(file)

    file.close()

    return json_data


def find_element(driver, website_url):
    """
    `website_url`에 해당하는 블로그 게시물 HTML 요소를 탐색 후 반환합니다.

    :param driver: Chrome Driver
    :param website_url: 블로그 URL
    :return: 블로그 게시물 HTML 요소 | None
    """
    cards = driver.find_elements(By.TAG_NAME, "c-card")

    for card in cards:
        try:
            eyebrow = card.find_element(By.TAG_NAME, "c-frag")

            if eyebrow.text == website_url:
                return card
        except NoSuchElementException:
            pass

    return None


def find_anchor(element):
    """
    `element`에서 `a` 태그를 탐색 후 반환합니다.

    :param element: 탐색 대상
    :return: `a` 태그 | None
    """
    try:
        body = element.find_element(By.TAG_NAME, "c-doc-web")
        return body.find_element(By.TAG_NAME, "a")
    except NoSuchElementException:
        return None


if __name__ == '__main__':
    # Chrome Driver 생성
    driver = webdriver.Chrome()

    # 데이터 불러오기
    data = load_data()

    website_url = data["website_url"]
    queries = data["queries"]

    # 검색어를 순회하며 자동화를 수행합니다.
    for query in queries:
        url = make_url(query)

        # URL 접근
        driver.get(url)
        time.sleep(1)

        # 태그 분석 및 게시물 탐색
        element = find_element(driver, website_url)
        if element is None:
            print(f"해당 검색어({query})의 검색 결과로는 블로그 게시물을 찾지 못했습니다.")
            continue

        anchor = find_anchor(element)
        if anchor is None:
            print(f"해당 검색어({query})의 블로그 게시물 요소 내에서 `a` 태그를 찾지 못하였습니다.")
            continue

        # 블로그 게시물 열기 및 활성 탭 변경 후 1초 대기
        anchor.click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)

        # 블로그 게시물 탭 닫기 및 활성 탭 변경 후 0.25초 대기
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.25)

    # Chrome Driver 종료
    driver.quit()
