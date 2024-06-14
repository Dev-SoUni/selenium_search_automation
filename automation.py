import time
import json

from selenium import webdriver


def make_url(query):
    """
    `daum` 검색 URL을 생성해줍니다.

    :param query: 검색어 키워드
    :return: 검색 키워드가 포함된 URL
    """
    return f"https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&q={query}"


def load_data():
    """
    `./data/search.json` 파일을 읽어 반환합니다.

    :return: `search.json`
    """
    file = open("./data/search.json", "r")

    json_data = json.load(file)

    file.close()

    return json_data


if __name__ == '__main__':
    # Chrome Driver 생성
    driver = webdriver.Chrome()

    # 데이터 불러오기
    data = load_data()

    website_url = data["website_url"]
    queries = data["queries"]

    # 검색어를 순환하며 자동화를 수행합니다.
    for query in queries:
        url = make_url(query)

        driver.get(url)
        time.sleep(0.25)

    # Chrome Driver 종료
    driver.quit()
