import streamlit as st
import folium
from streamlit_folium import st_folium

# function
def format_money(amount):
    """숫자를 '억' 단위와 '만원'으로 포맷팅"""
    if amount >= 10000:
        억 = amount // 10000
        만 = amount % 10000
        if 만 == 0:
            return f'{억}억'
        else:
            return f'{억}억 {만}만원'
    else:
        return f'{amount}만원'

st.set_page_config(layout="wide")  # 전체 화면 넓게 사용

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🔍 검색 필터")

building_types = ['원룸', '투룸', '오피스텔', '아파트']
selected_types = []

st.sidebar.write("선호하는 건물 유형을 모두 선택하세요:")
for type in building_types:
    if st.sidebar.checkbox(type):
        selected_types.append(type)

st.sidebar.divider()

with st.sidebar.expander('구조 ･ 면적'):
    st.write('구조 ･ 면적 아직')
with st.sidebar.expander('옵션'):
    st.write('옵션 아직')

st.sidebar.divider()

with st.sidebar.expander('전세'):
    price = st.slider("전세금 (만원)", 1000, 30000, (3000, 1000), step = 200)
    min_text = format_money(price[0])
    max_text = format_money(price[1])
    st.text(f'최소 {min_text} ~ 최대 {max_text}')

with st.sidebar.expander('월세'):
    price = st.slider("보증금 (만원)", 500, 10000, (2000, 5000), step = 100)
    min_text = format_money(price[0])
    max_text = format_money(price[1])
    st.text(f'최소 {min_text} ~ 최대 {max_text}')
    
    price = st.slider("월세 (만원)", 10, 300, (30, 80), step = 10)
    min_text = format_money(price[0])
    max_text = format_money(price[1])
    st.text(f'최소 {min_text} ~ 최대 {max_text}')

col1, col2 = st.sidebar.columns([1, 1.7])
with col1:
    if st.button("초기화", use_container_width=True):
        st.write("초기화 됐습니다.")
with col2:
    if st.button("검색", use_container_width=True):
        st.write("검색 중입니다!")

# -----------------------------
# 상단 네비게이션 바
# -----------------------------
st.markdown("""
    <style>
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #2c3e50;
        color: white;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
        z-index: 1000;
        text-align: center;
    }
    .stApp {
        margin-top: 60px;
    }
    div.stButton > button:last-child {
    background-color: #33C3FF;
    color: white;
    font-weight: bold;
    }
    </style>
    <div class="navbar">🌎방구🌎 | 원룸 매물 검색 어플 | 셀렉 </div>
""", unsafe_allow_html=True)

# -----------------------------
# Folium 지도
# -----------------------------
# 지도 생성
m = folium.Map(location=[37.513083, 126.938559], zoom_start=16)

# 마커 추가 예시
loc=[37.5662952, 126.9779451] #위도,경도 #위도,경도
folium.Marker(location=loc).add_to(m)

# Streamlit에 표시
st_folium(m, use_container_width=True, height=800)