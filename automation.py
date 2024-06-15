import time
import json

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def make_url(query, page=1):
    """
    `daum` 검색 URL을 생성해줍니다.

    :param query: 검색어 키워드
    :return: 검색 키워드가 포함된 URL
    """
    return f"https://search.daum.net/search?w=fusion&col=blog&q={query}&DA=TWA&p={page}"


def load_data():
    """
    `./data/search.json` 파일을 읽어 반환합니다.

    :return: `search.json`
    """
    file = open("./data/search.json", "r")

    json_data = json.load(file)

    file.close()

    return json_data


def get_chrome_options():
    """
    `Chrome Driver` 옵션 값 생성

    :return: ChromeOptions
    """
    options = webdriver.ChromeOptions()

    # 매크로 탐지를 회피하기 위한 `UserAgent` 설정
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

    # 시크릿 모드 활성화
    options.add_argument("--incognito")

    return options


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


def search(driver, website_url, query, start_page, end_page):
    """
    페이지를 순차적으로 전환해가며 블로그 게시물을 탐색

    :param driver: Chrome Driver
    :param query: 검색어 키워드
    :param start_page: 탐색 시작 페이지
    :param end_page: 탐색 종료 페이지
    :return: 블로그 게시물 HTML 요소 | None
    """
    for current_page in range(start_page, end_page + 1):
        url = make_url(query, page=current_page)

        # URL 접근 후 0.25초 대기
        driver.get(url)
        time.sleep(0.25)

        # 태그 분석 및 게시물 탐색
        element = find_element(driver, website_url)

        if element:
            return element

    return None


if __name__ == '__main__':
    # Chrome Driver 생성
    driver = webdriver.Chrome(options=get_chrome_options())

    # 데이터 불러오기
    data = load_data()

    website_url = data["website_url"]
    start_page = data["start_page"]
    end_page = data["end_page"]
    queries = data["queries"]

    # 검색어를 순회하며 자동화를 수행합니다.
    for query in queries:
        # 블로그 게시물 탐색 (페이지를 전환해가며 탐색)
        element = search(driver=driver, website_url=website_url, query=query, start_page=start_page, end_page=end_page)
        if element is None:
            print(f"해당 검색어({query})의 검색 결과로는 블로그 게시물을 찾지 못했습니다.")
            continue

        anchor = find_anchor(element)
        if anchor is None:
            print(f"해당 검색어({query})의 블로그 게시물 요소 내에서 `a` 태그를 찾지 못하였습니다.")
            continue

        # 블로그 게시물 열기 및 활성 탭 변경 후 2초 대기
        anchor.click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)

        # 블로그 게시물 탭 닫기 및 활성 탭 변경 후 0.25초 대기
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.25)

    # Chrome Driver 종료
    driver.quit()
