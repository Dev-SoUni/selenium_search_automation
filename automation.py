import json

from common.selenium.driver import get_chrome_driver
from common.websites.daum import Daum
from common.websites.google import Google


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

    # 작업별로 순회하며 자동화를 수행
    for task in data["tasks"]:
        if task["website"] == "daum":
            daum = Daum(driver, task["website_url"])

            # 검색어를 순회하며 게시물 탐색 후 방문
            for query in task["queries"]:
                # 블로그 게시물 탐색 (페이지를 전환해가며 탐색)
                element = daum.search(query, task["start_page"], task["end_page"])
                if element is None:
                    print(f"해당 검색어({query})의 검색 결과로는 블로그 게시물을 찾지 못했습니다.")
                    continue

                # 블로그 게시물 방문
                daum.visit(element)

        if task["website"] == "google":
            google = Google(driver, task["website_url"])

            # 검색어를 순회하며 게시물 탐색 후 방문
            for query in task["queries"]:
                # 블로그 게시물 탐색 (페이지를 전환해가며 탐색)
                element = google.search(query)
                if element is None:
                    print(f"해당 검색어({query})의 검색 결과로는 블로그 게시물을 찾지 못했습니다.")
                    continue

                # 블로그 게시물 방문
                google.visit(element)

    # Chrome Driver 종료
    driver.quit()
