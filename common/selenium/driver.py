from selenium import webdriver


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


def get_chrome_driver():
    """
    Chrome Driver 생성

    :return: Chrome Driver
    """
    return webdriver.Chrome(options=get_chrome_options())
