import cx_Oracle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from konlpy.tag import Hannanum
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import datetime


def get_oracle_connection():
    # SID가 'xe'인 경우, sid 매개변수를 사용합니다.
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', sid='xe')
    connection = cx_Oracle.connect(user='base_man', password='1111', dsn=dsn_tns)
    return connection


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
    wait = WebDriverWait(driver, 20)  # 대기 시간 20초로 설정

    while True:
        try:
            # 뉴스 리스트가 로드될 때까지 기다립니다.
            list_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#_newsList > ul > li")))

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

                # 뉴스 내용이 로드될 때까지 기다립니다.
                try:
                    content = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '#comp_news_article > div._article_content'))).text
                except Exception as e:
                    content = f"내용 추출 실패: {e}"

                news_details.append({'title': title, 'content': content, 'href': href})
                driver.back()

            all_news_data.extend(news_details)

            # 다음 페이지 버튼이 활성화되었는지 확인 후 클릭
            try:
                next_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#_pageList > a.next")))
                if next_page.is_displayed() and next_page.is_enabled():
                    next_page.click()
                else:
                    break
            except Exception as e:
                print(f"다음 페이지 오류: {e}")
                break

        except Exception as e:
            print(f"페이지 로딩 오류: {e}")
            break

    driver.quit()
    return team_code, all_news_data


def extract_keywords(content):
    hannanum = Hannanum()
    nouns = hannanum.nouns(content)
    filtered_nouns = [noun for noun in nouns if len(noun) > 1]
    return ', '.join(filtered_nouns)


def save_news_to_db(team_code, news_date, news_details):
    connection = get_oracle_connection()
    cursor = connection.cursor()

    formatted_date = news_date.strftime('%Y-%m-%d')

    for news in news_details:
        if isinstance(news, dict):
            title = news.get('title', '')
            content = news.get('content', '')
            href = news.get('href', '')
            keywords = extract_keywords(content)

            try:
                cursor.execute("""
                    INSERT INTO news_summary (id, team_code, news_date, title, keywords, href)
                    VALUES (news_summary_seq.NEXTVAL, :team_code, :news_date, :title, :keywords, :href)
                    """, team_code=team_code, news_date=formatted_date, title=title, keywords=keywords, href=href)

                connection.commit()
            except cx_Oracle.IntegrityError as e:
                print(f"Integrity error: {e}. Skipping duplicate entry.")
                connection.rollback()
            except Exception as e:
                print(f"Error occurred: {e}")
                connection.rollback()
        else:
            print(f"Unexpected data format: {news}")

    cursor.close()
    connection.close()


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
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for team_name, team_code in team_codes.items():
                print(f"{team_name} 팀의 {current_date} 뉴스 데이터를 수집하고 있습니다...")
                futures.append(executor.submit(fetch_news_for_team, team_code, current_date))

            for future in concurrent.futures.as_completed(futures):
                team_code, news_details = future.result()
                save_news_to_db(team_code, current_date, news_details)
                print(f"{team_code} 팀의 {current_date} 뉴스 데이터 수집 및 저장이 완료되었습니다.")
        current_date += datetime.timedelta(days=1)


# 날짜를 임의로 설정하여 수집 실행
if __name__ == "__main__":
    start_date = datetime.date(2024, 8, 15)  # 예시: 시작 날짜
    end_date = datetime.date(2024, 8, 20)  # 예시: 종료 날짜

    collect_news_for_date_range(start_date, end_date)
