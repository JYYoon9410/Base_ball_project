import streamlit as st
import cx_Oracle
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Hannanum
import datetime
import io
import matplotlib.pyplot as plt


# 데이터베이스 연결 설정
def get_oracle_connection():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', sid='xe')
    connection = cx_Oracle.connect(user='base_man', password='1111', dsn=dsn_tns)
    return connection


# 특정 날짜 범위의 키워드와 뉴스 데이터를 데이터베이스에서 가져오는 함수
def fetch_news_and_keywords_from_db(start_date, end_date, team_code):
    connection = get_oracle_connection()
    cursor = connection.cursor()

    # 키워드 쿼리
    keywords_query = """
        SELECT keywords
        FROM news_summary
        WHERE news_date BETWEEN :start_date AND :end_date
        AND team_code = :team_code
    """

    # 뉴스 쿼리
    news_query = """
        SELECT title, href
        FROM news_summary
        WHERE news_date BETWEEN :start_date AND :end_date
        AND team_code = :team_code
    """

    cursor.execute(keywords_query, start_date=start_date, end_date=end_date, team_code=team_code)
    rows = cursor.fetchall()

    keywords = []
    for row in rows:
        # LOB 객체를 문자열로 변환
        keywords_str = row[0].read() if isinstance(row[0], cx_Oracle.LOB) else row[0]
        keywords.extend(keywords_str.split(', '))

    cursor.execute(news_query, start_date=start_date, end_date=end_date, team_code=team_code)
    news_rows = cursor.fetchall()

    cursor.close()
    connection.close()

    news_details = [{'title': row[0], 'href': row[1]} for row in news_rows]

    return keywords, news_details


# Streamlit 앱 설정
st.set_page_config(
    page_title="Home in Run",
    page_icon="./team_logo/baseball.png"
)

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

team_logo_path = "team_logo2/"

# 사이드바 메뉴 설정
st.sidebar.title("메뉴")
menu = st.sidebar.radio("선택하세요", ("메인페이지", "구단별 뉴스토픽 조회", "구단별 선수 조회"))

# 메인 페이지
if menu == "메인페이지":
    st.title("Home in Run")
    st.markdown("### Home in Run 메인페이지 입니다.")
    st.markdown("여기는 KBO 팀 페이지의 메인페이지입니다. 구단별 뉴스와 관련 정보를 확인할 수 있습니다.")

# 구단별 뉴스토픽 조회
elif menu == "구단별 뉴스토픽 조회":
    st.title("야구뉴스 한눈에")

    # 팀 코드 사전
    tabs = st.tabs(list(team_codes.keys()))

    for i, (team_name, team_code) in enumerate(team_codes.items()):
        with tabs[i]:
            # 로고와 제목, 설명을 같은 행에 배치
            col1, empty_col, col2 = st.columns([1, 0.5, 5])

            with col1:
                # 로고 이미지 표시
                st.image(f"{team_logo_path}{team_code.lower()}.png", width=150)

            with col2:
                # 팀 제목 및 설명
                st.header(f"{team_name} 팀 페이지")
                st.markdown("### 여기는 {} 팀 페이지입니다.".format(team_name))

            # 날짜 선택 및 조회 버튼을 상단에 배치
            st.markdown("### 기간별 뉴스 조회")  # 조회 섹션의 제목을 추가합니다.

            # 폼 설정
            with st.form(key=f"form_{team_code}"):
                col1, col2 = st.columns([4, 4])

                with col1:
                    start_date = st.date_input("시작 날짜", min_value=datetime.date(2020, 1, 1),
                                               max_value=datetime.date.today(), key=f"start_date_{team_code}")

                with col2:
                    end_date = st.date_input("종료 날짜", min_value=start_date,
                                             max_value=datetime.date.today(), key=f"end_date_{team_code}")

                submit_button = st.form_submit_button("조회")

                if submit_button:
                    if start_date > end_date:
                        st.error("종료 날짜는 시작 날짜보다 늦어야 합니다.")
                    else:
                        with st.spinner("키워드와 뉴스 데이터를 가져오는 중입니다..."):
                            # 선택한 날짜 범위와 팀 코드로 키워드 및 뉴스 데이터 로드
                            keywords, news_details = fetch_news_and_keywords_from_db(start_date, end_date, team_code)

                            if not keywords:
                                st.warning("해당 기간에 키워드가 없습니다.")
                            else:
                                # 워드 클라우드 생성
                                hannanum = Hannanum()
                                word_list = hannanum.nouns(' '.join(keywords))

                                font_path = 'KBO Dia Gothic_medium.ttf'  # 워드클라우드 폰트 설정 (사용자의 시스템에 맞는 경로로 변경 필요)
                                wordcloud = WordCloud(
                                    font_path=font_path,
                                    width=800,
                                    height=800,
                                    background_color="white"
                                ).generate_from_frequencies(Counter(word_list))

                                # 워드 클라우드 이미지 표시
                                st.image(wordcloud.to_array(), caption=f"{team_name} 관련 뉴스 워드 클라우드",
                                         use_column_width=True)

                                # 뉴스 제목 및 링크 표시 (페이지네이션)
                                num_per_page = 5
                                total_pages = (len(news_details) + num_per_page - 1) // num_per_page

                                page = st.selectbox("페이지 선택", range(1, total_pages + 1), key=f"page_select_{team_code}")
                                start_index = (page - 1) * num_per_page
                                end_index = min(page * num_per_page, len(news_details))

                                st.markdown("### 최신 뉴스")
                                for article in news_details[start_index:end_index]:
                                    st.markdown(f"[{article['title']}]({article['href']})")

# 추후 추가 예정 페이지
elif menu == "구단별 선수 조회":
    st.title("추후 추가 예정")
    tabs = st.tabs(list(team_codes.keys()))
    st.markdown("이 페이지는 추후 추가될 기능을 위한 공간입니다.")
