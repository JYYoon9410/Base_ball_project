import cx_Oracle
import urllib.request
from bs4 import BeautifulSoup


# Oracle 데이터베이스 연결 함수
def get_oracle_connection():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', sid='xe')
    connection = cx_Oracle.connect(user='base_man', password='1111', dsn=dsn_tns)
    return connection


# 팀 코드 매핑
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

# 웹 스크래핑 코드
html = urllib.request.urlopen('https://www.samsunglions.com/roster/roster_2_list.asp')
soup = BeautifulSoup(html, 'html.parser')
base_url = 'https://www.samsunglions.com'

found = soup.find_all("div", class_="list")
items = []

# 현재 스크래핑된 페이지가 '삼성' 팀의 '투수' 정보임을 가정
current_team = "삼성"
current_team_code = team_codes[current_team]
current_position = "투수"

for div in found:
    for li in div.find_all('li'):
        img_tag = li.find('img')
        text_span = li.find('span', class_='txt')

        if img_tag:
            img_src = img_tag.get('src')
            img_url = base_url + img_src
        else:
            img_url = "No image found"

        if text_span:
            text = text_span.get_text(separator=' ', strip=True)
        else:
            text = "No text found"

        items.append({
            'Image URL': img_url,
            'Text': text,
            'Team Name': current_team,
            'Team Code': current_team_code,
            'Position': current_position
        })

# Oracle Database에 데이터 삽입
try:
    conn = get_oracle_connection()
    cursor = conn.cursor()

    # 데이터 삽입
    for item in items:
        img_url = item['Image URL']
        text = item['Text']
        team_name = item['Team Name']
        team_code = item['Team Code']
        position = item['Position']

        cursor.execute('''
            INSERT INTO players (name, image_url, team_name, team_code, position) 
            VALUES (:1, :2, :3, :4, :5)
        ''', (text, img_url, team_name, team_code, position))

    conn.commit()

except cx_Oracle.DatabaseError as e:
    print(f"Database error occurred: {e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
