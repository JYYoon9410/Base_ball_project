import cx_Oracle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from konlpy.tag import Hannanum
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Oracle DB 연결 함수

def get_oracle_connection():
    # SID가 'xe'인 경우, sid 매개변수를 사용합니다.
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', sid='xe')
    connection = cx_Oracle.connect(user='base_man', password='1111', dsn=dsn_tns)
    return connection


# 뉴스 데이터 크롤링 함수
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
    wait = WebDriverWait(driver, 10)

    while True:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#_newsList > ul > li")))

        list_items = driver.find_elements(By.CSS_SELECTOR, "#_newsList > ul > li")
        news_data = []
        for item in list_items:
            try:
                link = item.find_element(By.CSS_SELECTOR, 'div > a')
                title = link.find_element(By.TAG_NAME, 'span').text
                href = link.get_attribute('href')
                news_data.append({'title': title, 'href': href})
            except Exception as e:
                print(f"뉴스 데이터 추출 실패: {e}")

        news_details = []
        for item in news_data:
            title = item['title']
            href = item['href']
            driver.get(href)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#comp_news_article > div._article_content')))

            try:
                content = driver.find_element(By.CSS_SELECTOR, '#comp_news_article > div._article_content').text
            except Exception as e:
                content = f"내용 추출 실패: {e}"
            news_details.append({'title': title, 'content': content, 'href': href})
            driver.back()
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#_newsList > ul > li")))

        all_news_data.extend(news_details)

        try:
            pagination_div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#_pageList")))
            next_links = pagination_div.find_elements(By.TAG_NAME, 'a')

            next_page_found = False
            for link in next_links:
                if link.text.isdigit() and int(link.text) > 1:
                    next_page_found = True
                    link.click()
                    wait.until(EC.staleness_of(pagination_div))
                    break

            if not next_page_found:
                break
        except Exception as e:
            print(f"다음 페이지 링크 클릭 실패: {e}")
            break

    driver.quit()

    # 데이터 형식 검토
    print(f"팀 코드: {team_code}")
    print(f"수집된 뉴스 데이터: {all_news_data}")

    return team_code, all_news_data


# Hannanum을 사용하여 키워드를 추출하는 함수
def extract_keywords(content):
    hannanum = Hannanum()
    nouns = hannanum.nouns(content)
    return ', '.join(nouns)


# 데이터베이스에 뉴스 데이터를 저장하는 함수
def save_news_to_db(team_code, date, news_details):
    connection = get_oracle_connection()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO news_summary (id, team_code, news_date, title, href, keywords)
    VALUES (news_summary_seq.NEXTVAL, :1, :2, :3, :4, :5)
    """

    for article in news_details:
        if isinstance(article, dict) and all(k in article for k in ('title', 'content', 'href')):
            title = article['title']
            content = article['content']
            href = article['href']
            keywords = extract_keywords(content)

            cursor.execute(insert_query, (team_code, date.strftime('%Y-%m-%d'), title, href, keywords))
        else:
            print(f"올바르지 않은 데이터 형식: {article}")

    connection.commit()
    cursor.close()
    connection.close()




# 뉴스 데이터를 날짜 범위에 대해 수집하는 함수
def collect_news_for_date_range(start_date, end_date):
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

    current_date = start_date
    while current_date <= end_date:
        for team_name, team_code in team_codes.items():
            print(f"{team_name} 팀의 {current_date} 뉴스 데이터를 수집하고 있습니다...")
            news_details = fetch_news_for_team(team_code, current_date)
            save_news_to_db(team_code, current_date, news_details)
            print(f"{team_name} 팀의 {current_date} 뉴스 데이터 수집 및 저장이 완료되었습니다.")
        current_date += datetime.timedelta(days=1)


# 날짜를 임의로 설정하여 수집 실행
if __name__ == "__main__":
    # 설정할 날짜 범위
    start_date = datetime.date(2024, 8, 27)  # 예시: 시작 날짜
    end_date = datetime.date(2024, 8, 27)  # 예시: 종료 날짜

    # 뉴스 데이터를 날짜 범위에 대해 수집
    collect_news_for_date_range(start_date, end_date)
