import streamlit as st
import os
import sys
import urllib.request
import json
import pandas as pd
from konlpy.tag import Hannanum
from wordcloud import WordCloud
from collections import Counter
from PIL import Image
import numpy as np
from wordcloud import ImageColorGenerator
import streamlit.components.v1 as components
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from konlpy.tag import Hannanum


client_id = "OrUJ2MMfI3mvNbkqNKua"
client_secret = "BTAN1Yk5uw"


st.set_page_config(
    page_title="Home in Run",
    page_icon= "./team_logo/baseball.png"
)


# 팀 로고 이미지 경로 설정
team_logo_path = "team_logo/"

# 메인 타이틀
st.title("KBO 팀 페이지")

tabs = st.tabs(["두산", "삼성", "롯데", "LG", "KIA","한화","NC","SSG","키움","KT"])

with tabs[0]:
    st.header("두산 베어스")
    st.image(f"{team_logo_path}doosan.png", caption="두산 베어스", use_column_width=True)
    st.write("여기는 두산 베어스 팀 페이지입니다.")
    # 추가 정보 입력

with tabs[1]:  # 삼성 라이온즈 탭
    col1, empty_col, col2 = st.columns([1, 0.5, 10])

    with col1:
        st.image(f"{team_logo_path}samsung.png", width=90)
    with col2:
        st.header("삼성 라이온즈")
    st.markdown("## 여기는 삼성 라이온즈 팀 페이지입니다.")

    # 크롬 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음

    # ChromeDriver 경로 설정
    service = Service(ChromeDriverManager().install())

    # Selenium으로 브라우저 열기
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 웹 페이지 열기
    url = 'https://sports.news.naver.com/kbaseball/news/index?date=20240827&isphoto=N&type=team&team=SS'
    driver.get(url)

    # 페이지 로드 완료까지 대기
    time.sleep(3)

    # 뉴스 항목을 포함하는 리스트 요소 선택
    list_items = driver.find_elements(By.CSS_SELECTOR, "#_newsList > ul > li")

    # 뉴스 제목 및 링크 저장 리스트
    news_data = []

    # 각 항목을 반복하며 뉴스 제목과 링크 추출
    for item in list_items:
        # 링크 요소를 찾기
        link = item.find_element(By.CSS_SELECTOR, 'div > a')
        # 제목과 링크 추출
        title = link.find_element(By.TAG_NAME, 'span').text
        href = link.get_attribute('href')
        news_data.append({'title': title, 'href': href})

    # 뉴스 제목 및 내용 저장 리스트
    news_details = []

    for item in news_data:
        title = item['title']
        href = item['href']

        # 뉴스 상세 페이지 열기
        driver.get(href)
        time.sleep(3)

        # 뉴스 내용 추출
        try:
            content = driver.find_element(By.CSS_SELECTOR, '#comp_news_article > div._article_content').text
        except Exception as e:
            content = f"내용 추출 실패: {e}"  # 내용 추출 실패 시 오류 메시지

        # 뉴스 제목과 내용을 리스트에 추가
        news_details.append({'title': title, 'content': content})

        # 원래 페이지로 돌아가기
        driver.back()
        time.sleep(3)

    # 브라우저 닫기
    driver.quit()

    # 뉴스 제목 및 내용 출력
    # for item in news_details:
    #     print(f"Title: {item['title']}")
    #     print(f"Content: {item['content']}")
    #     print("\n")

    hannanum = Hannanum()

    # 뉴스 기사 내용에서 명사 추출
    temp = []
    for article in news_details:
        content = article['content']
        nouns = hannanum.nouns(content)
        temp.append(nouns)


    # 명사 추출 결과 일부 출력
    # print(temp[:1])

    def flatten(l):
        flatList = []
        for elem in l:
            if type(elem) == list:
                for e in elem:
                    flatList.append(e)
            else:
                flatList.append(elem)
        return flatList


    word_list = flatten(temp)
    word_list[:1]

    from wordcloud import WordCloud
    from collections import Counter

    font_path = 'KBO Dia Gothic_medium.ttf'

    wordcloud = WordCloud(
        font_path=font_path,
        width=800,
        height=800,
        background_color="white"
    )

    count = Counter(word_list)
    wordcloud = wordcloud.generate_from_frequencies(count)


    def __array__(self):
        """Convert to numpy array.
        Returns
        -------
        image : nd-array size (width, height, 3)
            Word cloud image as numpy matrix.
        """
        return self.to_array()


    def to_array(self):
        """Convert to numpy array.
        Returns
        -------
        image : nd-array size (width, height, 3)
            Word cloud image as numpy matrix.
        """
        return np.array(self.to_image())


    array = wordcloud.to_array()
    count = Counter(word_list)

    wc_moon = WordCloud(
    font_path=font_path,
    width=80,
    height=80,
    background_color="white"
)
    wc_moon = wc_moon.generate_from_frequencies(count)

    st.image(wc_moon.to_image(), caption="삼성 라이온즈 관련 뉴스 워드 클라우드", use_column_width=True)

with tabs[2]:
    st.header("롯데 자이언츠")
    st.image(f"{team_logo_path}lotte.png", caption="롯데 자이언츠", use_column_width=True)
    st.write("여기는 롯데 자이언츠 팀 페이지입니다.")


with tabs[3]:
    st.header("LG 트윈스")
    st.image(f"{team_logo_path}lg.png", caption="LG 트윈스", use_column_width=True)
    st.write("여기는 LG 트윈스 팀 페이지입니다.")
    # 추가 정보 입력

with tabs[4]:
    st.header("KIA 타이거즈")
    st.image(f"{team_logo_path}kia.png", caption="KIA 타이거즈", use_column_width=True)
    st.write("여기는 KIA 타이거즈 팀 페이지입니다.")

with tabs[5]:
    st.header("한화 이글스")
    st.image(f"{team_logo_path}hanwha.png", caption="한화 이글스", use_column_width=True)
    st.write("여기는 한화 이글스 팀 페이지입니다.")

with tabs[6]:
    st.header("NC 다이노스")
    st.image(f"{team_logo_path}nc.png", caption="NC 다이노스", use_column_width=True)
    st.write("여기는 NC 다이노스 팀 페이지입니다.")

with tabs[7]:
    st.header("SSG 랜더스")
    st.image(f"{team_logo_path}ssg.png", caption="SSG 랜더스", use_column_width=True)
    st.write("여기는SSG 랜더스 팀 페이지입니다.")

with tabs[8]:
    st.header("키움 히어로즈")
    st.image(f"{team_logo_path}kiwoom.png", caption="키움 히어로즈", use_column_width=True)
    st.write("여기는 키움 히어로즈 팀 페이지입니다.")

with tabs[9]:
    st.header("KT 위즈")
    st.image(f"{team_logo_path}kt.png", caption="KT 위즈", use_column_width=True)
    st.write("여기는 KT 위즈 팀 페이지입니다.")
