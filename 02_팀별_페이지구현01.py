import streamlit as st

# 메인 타이틀
st.title("KBO 팀 페이지")
team_logo_path = "team_logo/"
# 팀별 아이콘 클릭 시 페이지 전환
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)  # 3개의 컬럼으로 나누어 아이콘을 배치합니다.

with col1:
    st.image(f"{team_logo_path}doosan.png", caption='두산 베어스', use_column_width=True)
    if st.button("두산 베어스"):
        st.header("두산 베어스")
        st.write("여기는 두산 베어스 팀 페이지입니다.")
        # 추가적인 팀 정보나 콘텐츠를 여기에 입력합니다.

with col2:
    st.image(f"{team_logo_path}samsung.png", caption='삼성 라이온즈', use_column_width=True)
    if st.button("삼성 라이온즈"):
        st.header("삼성 라이온즈")
        st.write("여기는 삼성 라이온즈 팀 페이지입니다.")
        # 추가적인 팀 정보나 콘텐츠를 여기에 입력합니다.

with col3:
    st.image(f"{team_logo_path}lotte.png", caption='롯데 자이언츠', use_column_width=True)
    if st.button("롯데 자이언츠"):
        st.header("롯데 자이언츠")
        st.write("여기는 롯데 자이언츠 팀 페이지입니다.")
with col4:
    st.image(f"{team_logo_path}hanwha.png", caption='한화 이글스', use_column_width=True)
    if st.button("한화 이글스"):
        st.header("한화 이글스")
        st.write("여기는 한화 이글스 팀 페이지입니다.")
with col5:
    st.image(f"{team_logo_path}kia.png", caption='기아 타이거즈', use_column_width=True)
    if st.button("기아 타이거즈"):
        st.header("기아 타이거즈")
        st.write("여기는 기아 타이거즈 팀 페이지입니다.")

with col6:
    st.image(f"{team_logo_path}kiwoom.png", caption='키움 히어로즈', use_column_width=True)
    if st.button("키움 히어로즈"):
        st.header("키움 히어로즈")
        st.write("여기는 키움 히어로즈 팀 페이지입니다.")

with col7:
    st.image(f"{team_logo_path}lg.png", caption='엘지 트윈즈', use_column_width=True)
    if st.button("엘지 트윈즈"):
        st.header("엘지 트윈즈")
        st.write("여기는 엘지 트윈즈 팀 페이지입니다.")

with col8:
    st.image(f"{team_logo_path}nc.png", caption='엔씨 다이노스', use_column_width=True)
    if st.button("엔씨 다이노스"):
        st.header("엔씨 다이노스")
        st.write("여기는 엔씨 다이노스 팀 페이지입니다.")

with col9:
    st.image(f"{team_logo_path}ssg.png", caption='SSG 랜더스', use_column_width=True)
    if st.button("SSG 랜더스"):
        st.header("SSG 랜더스")
        st.write("여기는 SSG 랜더스 팀 페이지입니다.")

with col10:
    st.image(f"{team_logo_path}kt.png", caption='KT 위즈', use_column_width=True)
    if st.button("KT 위즈"):
        st.header("KT 위즈")
        st.write("여기는 KT 위즈 팀 페이지입니다.")