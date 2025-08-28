# bangoo_full_embed.py
# 회원가입/로그인/게스트 → 셀렉(매물검색) 올인원 Streamlit 앱

import streamlit as st
import datetime
import folium
from streamlit_folium import st_folium
import time


st.set_page_config(page_title='0827TEST') 
# -------------------- 공통 헤더 --------------------
def app_header(title="🌎방구🌎 | 원룸 매물 검색 어플"):
    st.markdown(f"""
        <style>
        .navbar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #fffff;
            color: black;
            padding: 12px;
            font-size: 18px;
            font-weight: bold;
            z-index: 1000;
            text-align: left;
        }}
        .stApp {{
            margin-top: 60px; /* 네비게이션 바 높이만큼 상단 여백 추가 */
        }}
        </style>
        <div class="navbar">{title}</div>
    """, unsafe_allow_html=True)

# -------------------- 버튼 스타일 --------------------
st.markdown("""
<style>
/* 모든 기본 버튼에 연한 살구색 배경 */
div.stButton > button {
  background: #ffe3d9; 
  border: 1px solid #ffd2c5; 
  color: #222;
  border-radius: 8px; 
  font-weight: 700; 
  height: 40px;
  transition: all 0.2s ease;
}
div.stButton > button:hover {
  background: #ffb89f !important;
  border: 1px solid #ff9d7a !important;
}
div.stButton > button:active {
  background: #ff9d7a !important;
  border: 1px solid #ff8355 !important;
}
/* 게스트 버튼 (회색) */
button[kind="secondary"] { 
  background: #ddd !important; 
  border-color: #d0d0d0 !important; 
}
button[kind="secondary"]:hover { 
  background: #888 !important; 
  border-color: #777 !important; 
}
button[kind="secondary"]:active { 
  background: #666 !important; 
  border-color: #555 !important; 
}
</style>
""", unsafe_allow_html=True)

# -------------------- 세션 상태 --------------------
if "step" not in st.session_state:
    st.session_state["step"] = "메인"

def go(step: str):
    st.session_state["step"] = step
    st.rerun()

# -------------------- 페이지 정의 --------------------
def page_home():
    app_header("🌎방구🌎 | 메인 페이지")
    st.markdown(
        """
        <div style="text-align:center; padding: 60px 0 40px 0;">
            <h1 style="font-size: 48px; margin-bottom: 16px; font-weight: 800;">방구</h1>
            <p style="font-size:20px; color: #666; margin-bottom: 50px;">사회 초년생들을 위한 원룸 구하기 서비스</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        login_col, signup_col = st.columns(2, gap="medium")
        with login_col:
            if st.button("로그인", key="home_login", type="primary", use_container_width=True):
                go("로그인")
        with signup_col:
            if st.button("회원가입", key="home_signup", type="primary", use_container_width=True):
                go("회원가입")
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        guest_col1, guest_col2, guest_col3 = st.columns([0.5, 1, 0.5])
        with guest_col2:
            if st.button("게스트로 이용", key="home_guest", type="secondary", use_container_width=True):
                st.session_state["guest_mode"] = True
                st.info("게스트로 이용 시 일부 기능이 제한됩니다")
                time.sleep(1.5)
                go("셀렉")

def page_signup():
    app_header("🌎방구🌎 | 회원가입")
    st.header("회원가입")
    st.text_input("아이디", key="su_id")
    st.text_input("비밀번호", type="password", key="su_pw")
    st.text_input("닉네임", key="su_nick")
    birth = st.date_input("생일", value=datetime.date(2000, 1, 1), key="su_birth")
    st.selectbox("성별", ["성별 선택", "남성", "여성", "기타/응답안함"], key="su_gender")
    if st.button("회원가입", key="signup_submit", type="primary", use_container_width=True):
        st.success(f"회원가입 완료! 선택한 생일: {birth}")
        st.session_state["guest_mode"] = False
        go("셀렉")
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        if st.button("뒤로가기", key="signup_back"):
            go("메인")

def page_login():
    app_header("🌎방구🌎 | 로그인")
    st.header("로그인")
    st.text_input("아이디", key="li_id")
    st.text_input("비밀번호", type="password", key="li_pw")
    if st.button("로그인", key="login_submit", type="primary", use_container_width=True):
        st.success("로그인 성공 (데모)")
        st.session_state["guest_mode"] = False
        go("셀렉")
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        if st.button("뒤로가기", key="login_back"):
            go("메인")
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <span style='cursor: pointer; text-decoration: underline;'>[아이디 찾기]</span>
            &nbsp;&nbsp;&nbsp;
            <span style='cursor: pointer; text-decoration: underline;'>[비밀번호 찾기]</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

def page_guest():
    go("셀렉")

def page_select():
    app_header("🌎방구🌎 | 원룸 매물 검색")
    properties = [
        {
            "id": 1,
            "title": "월세 1000/65",
            "address": "서울특별시 동작구 상도동 294-87",
            "lat": 37.503, "lon": 126.945,
            "transaction": "보증금 1,000만원 / 월세 65만원",
            "management_fee": "10만원",
            "area": "19.84m² (6평)",
            "floor": "3층",
            "type": "분리형",
            "direction": "남동향",
            "heating": "개별난방",
            "cooling": "벽걸이 에어컨",
            "living_facilities": "냉장고, 세탁기, 싱크대, 책상, 옷장, 붙박이장, 신발장, 인덕션레인지",
            "security": "현관보안, CCTV, 비디오폰, 방범창",
            "etc": "화재경보기, 소화기"
        },
        {
            "id": 2,
            "title": "전세 2억 5000",
            "address": "서울특별시 강남구 역삼동 123-45",
            "lat": 37.500, "lon": 127.036,
            "transaction": "전세 2억 5,000만원",
            "management_fee": "없음",
            "area": "29.7m² (9평)",
            "floor": "5층",
            "type": "오픈형",
            "direction": "남향",
            "heating": "중앙난방",
            "cooling": "시스템 에어컨",
            "living_facilities": "냉장고, 세탁기",
            "security": "CCTV, 카드키",
            "etc": "화재경보기"
        }
    ]
    st.set_page_config(layout="wide")
    st.sidebar.markdown("## 🏠 매물 리스트")
    st.sidebar.markdown("---")
    if not properties:
        st.sidebar.warning("표시할 매물이 없습니다.")
    else:
        for prop in properties:
            with st.sidebar.container(border=True):
                st.markdown(f"#### {prop['title']}")
                st.caption(f"{prop['address']}")
                col1, col2 = st.columns(2)
                col1.text(f"거래: {prop['transaction']}")
                col2.text(f"관리비: {prop['management_fee']}")
                col1, col2 = st.columns(2)
                col1.text(f"면적: {prop['area']}")
                col2.text(f"층/구조: {prop['floor']} / {prop['type']}")
                with st.expander("상세 정보 보기"):
                    st.write(f"**방향:** {prop['direction']}")
                    st.write(f"**난방/냉방:** {prop['heating']} / {prop['cooling']}")
                    st.write(f"**생활시설:** {prop['living_facilities']}")
                    st.write(f"**보안:** {prop['security']}")
                    st.write(f"**기타:** {prop['etc']}")
    map_center = [37.513083, 126.938559]
    if properties:
        map_center = [properties[0]['lat'], properties[0]['lon']]
    m = folium.Map(location=map_center, zoom_start=15)
    for prop in properties:
        popup_html = f"""
        <b>{prop['title']}</b><br>
        {prop['address']}<br>
        거래: {prop['transaction']}<br>
        면적: {prop['area']}
        """
        folium.Marker(
            [prop['lat'], prop['lon']], 
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)
    st_folium(m, use_container_width=True, height=800)
    if st.button("뒤로가기"):
        go("메인")

# -------------------- 라우팅 --------------------
page = st.session_state["step"]
if page=="메인": page_home()
elif page=="회원가입": page_signup()
elif page=="로그인": page_login()
elif page=="게스트": page_guest()
elif page=="셀렉": page_select()
else: page_home()
