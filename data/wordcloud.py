from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import wordcloud
from konlpy.tag import Hannanum
from wordcloud import WordCloud
from collections import Counter


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

word_list=flatten(temp)
word_list[:1]



font_path = 'KBO Dia Gothic_medium.ttf'

wordcloud = WordCloud(
    font_path = font_path,
    width = 800,
    height = 800,
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


import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 10))
plt.imshow(array, interpolation="bilinear")
plt.show()
# fig.savefig('wordcloud.png')
