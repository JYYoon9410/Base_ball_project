#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
import urllib.request
import json
client_id = "OrUJ2MMfI3mvNbkqNKua"
client_secret = "BTAN1Yk5uw"
encText = urllib.parse.quote("삼성 라이온즈")


# In[2]:


url = "https://openapi.naver.com/v1/search/blog?&display=100&sort=sim&query=" + encText

#
# # In[3]:
#
#
# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id",client_id)
# request.add_header("X-Naver-Client-Secret",client_secret)
# response = urllib.request.urlopen(request)
# rescode = response.getcode()
# if(rescode==200):
#     response_body = response.read()
#     print(response_body.decode('utf-8'))
# else:
#     print("Error Code:" + rescode)
#
#
# # In[4]:
#
#
# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id",client_id)
# request.add_header("X-Naver-Client-Secret",client_secret)
# response = urllib.request.urlopen(request)
# rescode = response.getcode()
# if rescode == 200:
#     response_body = response.read()
#     decoded_body = response_body.decode('utf-8')
#
#     # JSON 데이터를 파싱하여 출력
#     data = json.loads(decoded_body)
#     for item in data['items']:
#         print(item['title'], item['description'])
# else:
#     print("Error Code:" + str(rescode))


# In[5]:


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
    
    # lines 리스트 출력 (확인용)
    for line in lines:
        print(line)
else:
    print("Error Code:" + str(rescode))


# In[6]:


import pandas as pd
from konlpy.tag import Hannanum


# In[7]:


hannanum = Hannanum()

temp = []
for line in lines:
    # '>' 문자를 제거
    clean_line = line.replace('>', '')
    
    # 명사 추출
    temp.append(hannanum.nouns(clean_line))

# 결과 출력 (확인용)
print(temp[:])


# In[8]:


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


# In[9]:


word_list=pd.Series([x for x in word_list if len(x)>1])
word_list.value_counts().head(10)


# In[10]:


from wordcloud import WordCloud
from collections import Counter

font_path = 'NanumBarunGothic.ttf'

wordcloud = WordCloud(
    font_path = font_path,
    width = 800,
    height = 800,
    background_color="white"
)

count = Counter(word_list)
wordcloud = wordcloud.generate_from_frequencies(count)


# In[11]:


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
fig.savefig('wordcloud.png')


# In[12]:


from PIL import Image
import numpy as np
from wordcloud import ImageColorGenerator

# image_name = '문재인대통령.PNG'
image_name = 'samsung.png'


target_image = Image.open(image_name) 

try:
    mask = Image.new("RGB", target_image.size, (255,255,255))
    mask.paste(target_image,target_image)
    mask = np.array(mask)
    print("mask 변환 방식1")
except:
    print(image_name)
    mask=np.array(Image.open(image_name))
    print("mask 변환 방식2")
finally:
    plt.imshow(target_image)


# In[13]:


count = Counter(word_list)

wc_moon = WordCloud(
    font_path = font_path,
    # mask=moon_mask,
    mask=mask,
    background_color="white"
)


# In[14]:


wc_moon = wc_moon.generate_from_frequencies(count)

plt.figure(figsize=(10,10))
plt.imshow(wc_moon,interpolation="bilinear")
plt.axis("off")
plt.show()

