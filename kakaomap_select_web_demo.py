import streamlit as st
import streamlit.components.v1 as components
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
# sidebar 
st.sidebar.title("🔍 검색 필터")
building_types = ['원룸', '투룸', '오피스텔', '아파트']
selected_types = []
st.sidebar.write("선호하는 건물 유형을 모두 선택하세요:")
for type in building_types:
    if st.sidebar.checkbox(type):
        selected_types.append(type)
st.sidebar.divider()
# 상세 옵션 선택
# 구조 면적
with st.sidebar.expander('구조 ･ 면적'):
    st.write('구조 ･ 면적 아직')
# 옵션
with st.sidebar.expander('옵션'):
    st.write('옵션 아직')
st.sidebar.divider()
# 전,월세 선택
# 전세 보증금
with st.sidebar.expander('전세'):
    price = st.slider("전세금 (만원)", 1000, 30000, (3000, 1000), step = 200)
    # 함수를 사용하여 슬라이더 값 포맷팅
    min_text = format_money(price[0])
    if price[1] == 100000:
        max_text = "1억 이상"
    else:
        max_text = format_money(price[1])
    # 텍스트
    st.text(f'최소 {min_text} ~ 최대 {max_text}')
# 월세 보증금, 월세
with st.sidebar.expander('월세'):
    price = st.slider("보증금 (만원)", 500, 10000, (2000, 5000), step = 100)
    # 함수를 사용하여 슬라이더 값 포맷팅
    min_text = format_money(price[0])
    if price[1] == 100000:
        max_text = "1억 이상"
    else:
        max_text = format_money(price[1])
    # 텍스트
    st.text(f'최소 {min_text} ~ 최대 {max_text}')
    
    price = st.slider("월세 (만원)", 10, 300, (30, 80), step = 10)
    # 함수를 사용하여 슬라이더 값 포맷팅
    min_text = format_money(price[0])
    if price[1] == 100000:
        max_text = "1억 이상"
    else:
        max_text = format_money(price[1])
    # 텍스트
    st.text(f'최소 {min_text} ~ 최대 {max_text}')
# 초기화, 확인 버튼
col1, col2 = st.sidebar.columns([1, 1.7])
with col1:
    if st.button("초기화", use_container_width=True):  # 폭을 컬럼에 맞춤
        st.write("초기화 됐습니다.")
with col2:
    if st.button("검색", use_container_width=True):   # 폭을 컬럼에 맞춤
        st.write("검색 중입니다!")
# 상단 네비게이션 바 (CSS + HTML)
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
        margin-top: 60px; /* navbar 높이만큼 본문 내려줌 */
    }
    /* 버튼 색 */
    div.stButton > button:last-child {
    background-color: #33C3FF;  /* 파랑 계열 */
    color: white;
    font-weight: bold;
    }
    </style>
    <div class="navbar">🌎방구🌎 | 원룸 매물 검색 어플 | 셀렉 </div>
""", unsafe_allow_html=True)
# 카카오맵 Web 도메인 등록해야 맵이 보임
# 카카오맵 HTML (풀스크린)
map_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script type="text/javascript"
        src="//dapi.kakao.com/v2/maps/sdk.js?appkey=78deb4edc691f1c8debe7086160df634"></script>
</head>
<body>
<div id="map" style="width:100%;height:100vh;"></div>
<script>
    var mapContainer = document.getElementById('map'); 
    var mapOption = { 
        center: new kakao.maps.LatLng(37.5665, 126.9780), 
        level: 5
    };
    var map = new kakao.maps.Map(mapContainer, mapOption); 
    // 마커 예시
    var marker = new kakao.maps.Marker({
        position: new kakao.maps.LatLng(37.5665, 126.9780)
    });
    marker.setMap(map);
</script>
</body>
</html>
"""
components.html(map_html, height=800)