import streamlit as st

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

with tabs[1]:
    st.header("삼성 라이온즈")
    st.image(f"{team_logo_path}samsung.png", caption="삼성 라이온즈", use_column_width=True)
    st.write("여기는 삼성 라이온즈 팀 페이지입니다.")
    # 추가 정보 입력

with tabs[2]:
    st.header("롯데 자이언츠")
    st.image(f"{team_logo_path}lotte.png", caption="롯데 자이언츠", use_column_width=True)
    st.write("여기는 롯데 자이언츠 팀 페이지입니다.")
    # 추가 정보 입력

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
