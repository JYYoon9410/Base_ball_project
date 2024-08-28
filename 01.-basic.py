import streamlit as st
import pandas as pd




# 사이드바에 페이지 선택 메뉴 생성
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Page 1", "Page 2"])

# Home 페이지
if page == "Home":
    st.title("Home")
    st.write("Welcome to the Home page!")

# Page 1
elif page == "Page 1":
    st.title("Page 1")
    st.write("Welcome to Page 1!")

# Page 2
elif page == "Page 2":
    st.title("Page 2")
    st.write("Welcome to Page 2!")