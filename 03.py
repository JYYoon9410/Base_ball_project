import streamlit as st

# 팀 로고 이미지 경로 설정
team_logo_path = "team_logo/"

# 메인 타이틀
st.title("KBO 팀 페이지")

# 사이드바에 KBO 팀 선택 메뉴 생성
teams = ["두산 베어스", "삼성 라이온즈", "롯데 자이언츠", "LG 트윈스", "KIA 타이거즈",
         "한화 이글스", "NC 다이노스", "SSG 랜더스", "키움 히어로즈", "KT 위즈"]

# 페이지 상태를 저장하기 위한 세션 상태 사용
if 'selected_team' not in st.session_state:
    st.session_state.selected_team = teams[0]  # 기본 선택된 팀은 첫 번째 팀

# 팀 선택 인터페이스 생성
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

with col1:
    if st.button("두산 베어스", key='doosan_button'):
        st.session_state.selected_team = "두산 베어스"
    st.image(f"{team_logo_path}doosan.png", caption='두산 베어스', use_column_width=True)

with col2:
    if st.button("삼성 라이온즈", key='samsung_button'):
        st.session_state.selected_team = "삼성 라이온즈"
    st.image(f"{team_logo_path}samsung.png", caption='삼성 라이온즈', use_column_width=True)

with col3:
    if st.button("롯데 자이언츠", key='lotte_button'):
        st.session_state.selected_team = "롯데 자이언츠"
    st.image(f"{team_logo_path}lotte.png", caption='롯데 자이언츠', use_column_width=True)

with col4:
    if st.button("LG 트윈스", key='LG_button'):
        st.session_state.selected_team = "LG 트윈스"
    st.image(f"{team_logo_path}lg.png", caption='LG 트윈스', use_column_width=True)

with col5:
    if st.button("KIA 타이거즈", key='KIA_button'):
        st.session_state.selected_team = "KIA 타이거즈"
    st.image(f"{team_logo_path}kia.png", caption='KIA 타이거즈', use_column_width=True)

with col6:
    if st.button("한화 이글스", key='hanwha_button'):
        st.session_state.selected_team = "한화 이글스"
    st.image(f"{team_logo_path}hanwha.png", caption='한화 이글스', use_column_width=True)

with col7:
    if st.button("NC 다이노스", key='NC_button'):
        st.session_state.selected_team = "NC 다이노스"
    st.image(f"{team_logo_path}nc.png", caption='NC 다이노스', use_column_width=True)

with col8:
    if st.button("SSG 랜더스", key='SSG_button'):
        st.session_state.selected_team = "SSG 랜더스"
    st.image(f"{team_logo_path}ssg.png", caption='SSG 랜더스', use_column_width=True)

with col9:
    if st.button("키움 히어로즈", key='kiwoom_button'):
        st.session_state.selected_team = "키움 히어로즈"
    st.image(f"{team_logo_path}kiwoom.png", caption='키움 히어로즈', use_column_width=True)

with col10:
    if st.button("KT 위즈", key='KT_button'):
        st.session_state.selected_team = "KT 위즈"
    st.image(f"{team_logo_path}kt.png", caption='KT 위즈', use_column_width=True)


# 팀별 페이지 내용 표시
if st.session_state.selected_team == "두산 베어스":
    st.header("두산 베어스")
    st.write("여기는 두산 베어스 팀 페이지입니다.")
    # 여기에 두산 베어스에 대한 추가 정보를 입력합니다.

elif st.session_state.selected_team == "삼성 라이온즈":
    st.header("삼성 라이온즈")
    st.write("여기는 삼성 라이온즈 팀 페이지입니다.")
    # 여기에 삼성 라이온즈에 대한 추가 정보를 입력합니다.

elif st.session_state.selected_team == "롯데 자이언츠":
    st.header("롯데 자이언츠")
    st.write("여기는 롯데 자이언츠 팀 페이지입니다.")
    # 여기에 롯데 자이언츠에 대한 추가 정보를 입력합니다.

elif st.session_state.selected_team == "LG 트윈스":
    st.header("LG 트윈스")
    st.write("여기는 LG 트윈스 팀 페이지입니다.")
    # 여기에 LG 트윈스에 대한 추가 정보를 입력합니다.

elif st.session_state.selected_team == "KIA 타이거즈":
    st.header("KIA 타이거즈")
    st.write("여기는 KIA 타이거즈 팀 페이지입니다.")
    # 여기에 KIA 타이거즈에 대한 추가 정보를 입력합니다.

elif st.session_state.selected_team == "한화 이글스":
    st.header("한화 이글스")
    st.write("여기는 한화 이글스 팀 페이지입니다.")
    # 여기에 한화 이글스에 대한 추가 정보를 입력합니다.

elif st.session_state.selected_team == "NC 다이노스":
    st.header("NC 다이노스")
    st.write("여기는 NC 다이노스 팀 페이지입니다.")
    # 여기에 NC 다이노스에 대한 추가 정보를 입력합니다.

elif st.session_state.selected_team == "SSG 랜더스":
    st.header("SSG 랜더스")
    st.write("여기는 SSG 랜더스 팀 페이지입니다.")
    # 여기에 SSG 랜더스에 대한 추가 정보를 입력합니다.

elif st.session_state.selected_team == "키움 히어로즈":
    st.header("키움 히어로즈")
    st.write("여기는 키움 히어로즈 팀 페이지입니다.")
    # 여기에 키움 히어로즈에 대한 추가 정보를 입력합니다.

elif st.session_state.selected_team == "KT 위즈":
    st.header("KT 위즈")
    st.write("여기는 KT 위즈 팀 페이지입니다.")
    # 여기에 KT 위즈에 대한 추가 정보를 입력합니다.
