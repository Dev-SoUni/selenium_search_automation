import json

from common.selenium.driver import get_chrome_driver
from common.websites.daum import Daum


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
    driver = get_chrome_driver()

    # 데이터 불러오기
    data = load_data()

    website_url = data["website_url"]
    start_page = data["start_page"]
    end_page = data["end_page"]
    queries = data["queries"]

    # Daum 검색 인스턴스 생성
    daum = Daum(driver, website_url)

    # 검색어를 순회하며 자동화를 수행합니다.
    for query in queries:
        # 블로그 게시물 탐색 (페이지를 전환해가며 탐색)
        element = daum.search(query, start_page, end_page)
        if element is None:
            print(f"해당 검색어({query})의 검색 결과로는 블로그 게시물을 찾지 못했습니다.")
            continue

        # 블로그 게시물 방문
        daum.visit(element)

    # Chrome Driver 종료
    driver.quit()
