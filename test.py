import streamlit as st
import folium
from streamlit_folium import st_folium

# 상단 네비게이션 바 CSS
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
    .button-grid button {
    height: 100px;
    width: 100%;
    font-size: 18px;
    margin: 5px 0;
    }
    .button-grid .selected {
        background-color: #4CAF50;
        color: white;
    }
    .button-grid .not-selected {
        background-color: #f0f0f0;
        color: black;
    }
    </style>
    <div class="navbar">🌎방구🌎 | 원룸 매물 검색 어플 | 셀렉 </div>
""", unsafe_allow_html=True)

# format_money 함수 선언 (전,월세 가격)
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
    
# option_tab_1() 함수 선언
def option_tab_1():
    tab1, tab2, tab3 = st.tabs(['구조', '층 수 옵션', '전용 면적'])
    # Tab 1: 구조
    with tab1:
        # 2x2 그리드 만들기
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            if st.button("전체"):
                st.session_state['selected'] = "전체"

        with col2:
            if st.button("오픈형\n(방1)"):
                st.session_state['selected'] = "오픈형"

        with col3:
            if st.button("분리형\n(방1, 거실1)"):
                st.session_state['selected'] = "분리형"

        with col4:
            if st.button("복층형"):
                st.session_state['selected'] = "복층형"
                
        # 선택한 버튼 표시
        selected = st.session_state.get('selected', "선택 없음")
        st.write(f"선택한 타입: {selected}")

    # Tab 2: 층 수 옵션
    with tab2:
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            if st.button("전체", key="tab2_전체"):
                st.session_state['selected_floor'] = "전체"
        with col2:
            if st.button("지상층", key="tab2_지상층"):
                st.session_state['selected_floor'] = "지상층"
        with col3:
            if st.button("반지하", key="tab2_반지하"):
                st.session_state['selected_floor'] = "반지하"
        with col4:
            if st.button("옥탑", key="tab2_옥탑"):
                st.session_state['selected_floor'] = "옥탑"

        selected = st.session_state.get('selected_floor', "선택 없음")
        st.write(f"선택한 층: {selected}")

    # Tab 3: 전용 면적
    with tab3:
        # 2x4 배열: 8개 버튼
        col1, col2, col3, col4 = st.columns(4)
        col5, col6, col7, col8 = st.columns(4)

        area_buttons = ["전체", "10평 이하", "10평대", "20평대",
                        "30평대", "40평대", "50평대", "60평 이상"]

        keys = ["tab3_"+btn for btn in area_buttons]

        # 첫 줄
        for col, btn, key in zip([col1, col2, col3, col4], area_buttons[:4], keys[:4]):
            if col.button(btn, key=key):
                st.session_state['selected_area'] = btn

        # 두 번째 줄
        for col, btn, key in zip([col5, col6, col7, col8], area_buttons[4:], keys[4:]):
            if col.button(btn, key=key):
                st.session_state['selected_area'] = btn

        selected = st.session_state.get('selected_area', "선택 없음")
        st.write(f"선택한 면적: {selected}")

# option_tab_2() 함수 선언
def option_tab_2():
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("에어컨", key="option_에어컨"):
            st.session_state['selected_option'] = "에어컨"

    with col2:
        if st.button("냉장고", key="option_냉장고"):
            st.session_state['selected_option'] = "냉장고"

    with col3:
        if st.button("세탁기", key="option_세탁기"):
            st.session_state['selected_option'] = "세탁기"

    selected = st.session_state.get('selected_option', "선택 없음")
    st.write(f"선택한 옵션: {selected}")


st.set_page_config(layout="wide")  # 전체 화면 넓게 사용

# 사이드 바
st.sidebar.title("🔍 검색 필터")

building_types = ['원룸', '투룸', '오피스텔', '아파트']
selected_types = []

st.sidebar.write("선호하는 건물 유형을 모두 선택하세요:")
for type in building_types:
    if st.sidebar.checkbox(type):
        selected_types.append(type)

st.sidebar.divider()

# 구조 ･ 면적
with st.sidebar.expander('구조 ･ 면적'):
    option_tab_1()

# 옵션
with st.sidebar.expander('옵션'):
    option_tab_2()

# 주차 가능 토글 버튼
selected = st.sidebar.toggle('주차 가능만 보기')

st.sidebar.divider()

# 전세 가격 옵션
with st.sidebar.expander('전세'):
    price = st.slider("전세금 (만원)", 1000, 30000, (3000, 1000), step = 200)
    min_text = format_money(price[0])
    max_text = format_money(price[1])
    st.text(f'최소 {min_text} ~ 최대 {max_text}')

# 월세 가격 옵션
with st.sidebar.expander('월세'):
    price = st.slider("보증금 (만원)", 500, 10000, (2000, 5000), step = 100)
    min_text = format_money(price[0])
    max_text = format_money(price[1])
    st.text(f'최소 {min_text} ~ 최대 {max_text}')
    
    price = st.slider("월세 (만원)", 10, 300, (30, 80), step = 10)
    min_text = format_money(price[0])
    max_text = format_money(price[1])
    st.text(f'최소 {min_text} ~ 최대 {max_text}')

# 초기화, 검색 버튼
col1, col2 = st.sidebar.columns([1, 1.7])
with col1:
    if st.button("초기화", use_container_width=True):
        # session_state에 저장된 모든 선택 값들을 초기 상태로 변경합니다.
        st.session_state['selected'] = "전체"
        st.session_state['selected_floor'] = "전체"
        st.session_state['selected_area'] = "전체"
        
        # 'selected_option'은 '전체'가 없으므로 key 자체를 삭제하여 초기 상태로 만듭니다.
        if 'selected_option' in st.session_state:
            del st.session_state['selected_option']
            
        st.success("필터가 초기화되었습니다.") # 사용자에게 초기화 완료를 명확히 알려줍니다.

with col2:
    if st.button("검색", use_container_width=True):
        st.write("검색 중 입니다!")

# Folium 지도, 지도 생성
m = folium.Map(location=[37.513083, 126.938559], zoom_start=16)

# 마커 추가 예시
loc=[37.5662952, 126.9779451] 
folium.Marker(location=loc).add_to(m)

# Streamlit에 표시
st_folium(m, use_container_width=True, height=800)