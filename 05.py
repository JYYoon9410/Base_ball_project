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


    # 구글 트렌드 검색
    # google_trends_code = """
    #     <script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/3826_RC01/embed_loader.js"></script>
    #     <script type="text/javascript">
    #         trends.embed.renderExploreWidget("RELATED_TOPICS", {"comparisonItem":[{"keyword":"삼성 라이온즈","geo":"KR","time":"now 1-d"}],"category":0,"property":""}, {"exploreQuery":"q=%EC%82%BC%EC%84%B1%20%EB%9D%BC%EC%9D%B4%EC%98%A8%EC%A6%88&date=now%201-d&geo=KR&hl=ko","guestPath":"https://trends.google.co.kr:443/trends/embed/"});
    #     </script>
    #     """
    # # Streamlit components 사용하여 HTML 삽입
    # components.html(google_trends_code, height=600)  # 높이를 원하는 크기로 조절할 수 있습니다.

    encText = urllib.parse.quote("삼성 라이온즈")
    url = "https://openapi.naver.com/v1/search/news?&display=100&sort=sim&query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        decoded_body = response_body.decode('utf-8')

        # JSON 데이터를 파싱하여 출력
        data = json.loads(decoded_body)
        lines = []
        for item in data['items']:
            # 제목과 링크를 합쳐서 한 줄의 문자열로 저장
            line = f"{item['title']} {item['description']}"
            lines.append(line)
    else:
        print("Error Code:" + str(rescode))
    hannanum = Hannanum()

    temp = []
    for line in lines:
        # '>' 문자를 제거
        clean_line = line.replace('>', '')

        # 명사 추출
        temp.append(hannanum.nouns(clean_line))


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
    word_list = pd.Series([x for x in word_list if len(x) > 1])
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
    width=800,
    height=800,
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
