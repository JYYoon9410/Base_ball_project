import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Hannanum
import time
import numpy as np

st.set_page_config(
    page_title="Home in Run",
    page_icon="./team_logo2/baseball.png"
)

# 팀 로고 이미지 경로 설정
team_logo_path = "team_logo2/"

# 메인 타이틀
st.title("KBO 팀 페이지")

# 팀 코드 사전
team_codes = {
    "두산": "OB",
    "삼성": "SS",
    "롯데": "LT",
    "LG": "LG",
    "KIA": "HT",
    "한화": "HH",
    "NC": "NC",
    "SSG": "SK",
    "키움": "WO",
    "KT": "KT"
}

tabs = st.tabs(list(team_codes.keys()))

# 크롬 옵션 설정 및 뉴스 데이터 로드 함수 정의
def load_news_data(team_code):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f'https://sports.news.naver.com/kbaseball/news/index?date=20240827&isphoto=N&type=team&team={team_code}'
    driver.get(url)

    time.sleep(3)
    list_items = driver.find_elements(By.CSS_SELECTOR, "#_newsList > ul > li")

    news_data = []
    for item in list_items:
        link = item.find_element(By.CSS_SELECTOR, 'div > a')
        title = link.find_element(By.TAG_NAME, 'span').text
        href = link.get_attribute('href')
        news_data.append({'title': title, 'href': href})

    news_details = []
    for item in news_data:
        title = item['title']
        href = item['href']
        driver.get(href)
        time.sleep(3)
        try:
            content = driver.find_element(By.CSS_SELECTOR, '#comp_news_article > div._article_content').text
        except Exception as e:
            content = f"내용 추출 실패: {e}"
        news_details.append({'title': title, 'content': content})
        driver.back()
        time.sleep(3)

    driver.quit()
    return news_details

# 리스트 평탄화 함수
def flatten(l):
    flatList = []
    for elem in l:
        if type(elem) == list:
            for e in elem:
                flatList.append(e)
        else:
            flatList.append(elem)
    return flatList

# 각 팀에 대한 탭 설정
for i, (team_name, team_code) in enumerate(team_codes.items()):
    with tabs[i]:
        st.header(f"{team_name} 팀 페이지")
        st.image(f"{team_logo_path}{team_code.lower()}.png", caption=f"{team_name}", use_column_width=True)
        st.write(f"여기는 {team_name} 팀 페이지입니다.")

        # 뉴스 데이터 로드 및 처리
        news_details = load_news_data(team_code)

        hannanum = Hannanum()
        temp = []
        for article in news_details:
            content = article['content']
            nouns = hannanum.nouns(content)
            temp.append(nouns)

        word_list = flatten(temp)

        # 워드 클라우드 생성
        font_path = 'KBO Dia Gothic_medium.ttf'
        wordcloud = WordCloud(
            font_path=font_path,
            width=800,
            height=800,
            background_color="white"
        )

        count = Counter(word_list)
        wordcloud = wordcloud.generate_from_frequencies(count)

        # Streamlit에 이미지 표시
        st.image(wordcloud.to_array(), caption=f"{team_name} 관련 뉴스 워드 클라우드", use_column_width=True)
