import streamlit as st

# 메인 타이틀
st.title("KBO 팀 페이지")

# 사이드바에 KBO 팀 선택 메뉴 생성
teams = ["두산 베어스", "삼성 라이온즈", "롯데 자이언츠", "LG 트윈스", "KIA 타이거즈",
         "한화 이글스", "NC 다이노스", "SSG 랜더스", "키움 히어로즈", "KT 위즈"]
selected_team = st.sidebar.selectbox("팀을 선택하세요", teams)

# 팀 별 페이지
if selected_team == "두산 베어스":
    st.header("두산 베어스")
    st.write("여기는 두산 베어스 팀 페이지입니다.")
    # 여기에 두산 베어스에 대한 추가 정보를 입력합니다.

elif selected_team == "삼성 라이온즈":
    st.header("삼성 라이온즈")
    st.write("여기는 삼성 라이온즈 팀 페이지입니다.")
    # 여기에 삼성 라이온즈에 대한 추가 정보를 입력합니다.

elif selected_team == "롯데 자이언츠":
    st.header("롯데 자이언츠")
    st.write("여기는 롯데 자이언츠 팀 페이지입니다.")
    # 여기에 롯데 자이언츠에 대한 추가 정보를 입력합니다.

elif selected_team == "LG 트윈스":
    st.header("LG 트윈스")
    st.write("여기는 LG 트윈스 팀 페이지입니다.")
    # 여기에 LG 트윈스에 대한 추가 정보를 입력합니다.

elif selected_team == "KIA 타이거즈":
    st.header("KIA 타이거즈")
    st.write("여기는 KIA 타이거즈 팀 페이지입니다.")
    # 여기에 KIA 타이거즈에 대한 추가 정보를 입력합니다.

elif selected_team == "한화 이글스":
    st.header("한화 이글스")
    st.write("여기는 한화 이글스 팀 페이지입니다.")
    # 여기에 한화 이글스에 대한 추가 정보를 입력합니다.

elif selected_team == "NC 다이노스":
    st.header("NC 다이노스")
    st.write("여기는 NC 다이노스 팀 페이지입니다.")
    # 여기에 NC 다이노스에 대한 추가 정보를 입력합니다.

elif selected_team == "SSG 랜더스":
    st.header("SSG 랜더스")
    st.write("여기는 SSG 랜더스 팀 페이지입니다.")
    # 여기에 SSG 랜더스에 대한 추가 정보를 입력합니다.

elif selected_team == "키움 히어로즈":
    st.header("키움 히어로즈")
    st.write("여기는 키움 히어로즈 팀 페이지입니다.")
    # 여기에 키움 히어로즈에 대한 추가 정보를 입력합니다.

elif selected_team == "KT 위즈":
    st.header("KT 위즈")
    st.write("여기는 KT 위즈 팀 페이지입니다.")
    # 여기에 KT 위즈에 대한 추가 정보를 입력합니다.
