import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Hannanum
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import datetime

st.set_page_config(
    page_title="Home in Run",
    page_icon="./team_logo/baseball.png"
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

# 뉴스 데이터 크롤링 함수 정의
def fetch_news_for_team(team_code, date):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    formatted_date = date.strftime('%Y%m%d')
    url = f'https://sports.news.naver.com/kbaseball/news/index?date={formatted_date}&isphoto=N&type=team&team={team_code}'
    driver.get(url)

    all_news_data = []
    while True:
        time.sleep(3)  # Wait for page load

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
            news_details.append({'title': title, 'content': content, 'href': href})
            driver.back()
            time.sleep(1)

        all_news_data.extend(news_details)

        try:
            # Check if there's a next page
            next_page = driver.find_element(By.CSS_SELECTOR, "#_pageList > a.next")
            if next_page.is_displayed():
                next_page.click()
            else:
                break
        except Exception as e:
            break

    driver.quit()
    return team_code, all_news_data

# 병렬 처리로 모든 팀의 뉴스를 가져오기
def load_all_news_data(team_codes, date):
    news_results = {}
    with ThreadPoolExecutor(max_workers=len(team_codes)) as executor:
        futures = {executor.submit(fetch_news_for_team, team_code, date): team_code for team_code in team_codes.values()}
        for future in as_completed(futures):
            team_code, news_details = future.result()
            news_results[team_code] = news_details
    return news_results

# 각 팀에 대한 탭 설정
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

        # 날짜 선택 및 조회 버튼을 수직으로 배치
        st.markdown("### 뉴스 조회")  # 조회 섹션의 제목을 추가합니다.
        date_col, empty_col1, button_col = st.columns([4, 1, 3])  # 날짜 선택기와 조회 버튼을 수직으로 배치합니다.

        with date_col:
            selected_date = st.date_input("날짜 선택", min_value=datetime.date(2020, 1, 1), max_value=datetime.date.today(), key=f"date_input_{team_code}")

        with button_col:
            if st.button("조회", key=f"button_{team_code}"):
                with st.spinner("뉴스를 로드하는 중입니다..."):
                    # 선택한 날짜를 기반으로 뉴스 데이터 로드
                    news_details = load_all_news_data({team_name: team_code}, selected_date)[team_code]

                    hannanum = Hannanum()
                    temp = []
                    for article in news_details:
                        content = article['content']
                        nouns = hannanum.nouns(content)
                        temp.append(nouns)

                    word_list = [item for sublist in temp for item in sublist]

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

                    # 워드 클라우드 이미지 저장
                    st.session_state[team_code] = {
                        'wordcloud': wordcloud.to_array(),
                        'news_details': news_details
                    }  # 세션 상태에 워드클라우드와 뉴스 제목 및 링크 저장

        # 저장된 워드클라우드 및 뉴스 제목 표시
        if team_code in st.session_state and st.session_state[team_code] is not None:
            # 워드클라우드 표시
            st.image(st.session_state[team_code]['wordcloud'], caption=f"{team_name} 관련 뉴스 워드 클라우드", use_column_width=True)

            # 뉴스 제목 및 링크 표시
            news_details = st.session_state[team_code]['news_details']
            num_per_page = 5
            total_pages = (len(news_details) + num_per_page - 1) // num_per_page

            start_index = 0
            end_index = min(num_per_page, len(news_details))

            if len(news_details) > num_per_page:
                page = st.selectbox("페이지 선택", range(1, total_pages + 1), key=f"page_select_{team_code}")
                start_index = (page - 1) * num_per_page
                end_index = min(page * num_per_page, len(news_details))

            st.markdown("### 최신 뉴스")
            for article in news_details[start_index:end_index]:
                st.markdown(f"[{article['title']}]({article['href']})")
