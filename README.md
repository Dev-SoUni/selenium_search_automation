# 티스토리 게시물 탐색 및 조회 자동화

### ✋ 소개

`Daum` 포털 사이트에서 특정 블로그의 게시물을 탐색하여 조회하는 과정을 자동화해줍니다.  
`search.json` 파일 값을 수정하여 탐색 옵션을 쉽게 커스터마이징 할 수 있습니다.


### ⚒️ 기술 스택

- `Python`
- `Selenium`


### 🏁 시작하기

#### 준비 사항

- `Chrome (version 115+)` 브라우저가 반드시 설치되어 있어야 합니다.


#### 패키지 설치

- `requirements.txt` 파일 내에 정리되어있는 패키지를 설치합니다.  
  (가상 환경 내에서 설치할 것을 권장합니다.)

```shell
pip install -r requirements.txt
```


#### 탐색 옵션 설정

- `./data/search.json` 파일 내의 값을 통해 탐색 옵션을 수정할 수 있습니다.

```json
{
  // 블로그 URL
  "website_url": "ribbit-ribbit.tistory.com",
  // 탐색 시작 페이지
  "start_page": 1,
  // 탐색 종료 페이지
  "end_page": 10,
  // 검색어 목록 (순차적으로 탐색 과정을 거칩니다.)
  "queries": [
    "프로그래머스 level0 정수를 나선형으로 배치하기",
    "프로그래머스 level1 체육복"
  ]
}
```


#### 실행

```shell
python automation.py
```


### 🖇️ 참고

- [GitHub](https://github.com/Dev-SoUni)
- [티스토리](https://ribbit-ribbit.tistory.com/)
