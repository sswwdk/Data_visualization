import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 기본 설정
st.set_page_config(
    page_title='🌎방구🌎 | 원룸 매물 검색',
    layout="wide"  # 전체 화면을 넓게 사용
)

# --- CSS 스타일 ---
# 상단 네비게이션 바 및 기타 UI 요소 스타일링
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
        margin-top: 60px; /* 네비게이션 바 높이만큼 상단 여백 추가 */
    }
    </style>
    <div class="navbar">🌎방구🌎 | 원룸 매물 검색 어플</div>
""", unsafe_allow_html=True)

# --- 샘플 데이터 ---
# 실제 데이터베이스나 API에서 가져올 매물 데이터
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

# --- 사이드바 UI ---
# --- 매물 리스트 (Streamlit 위젯 사용) ---
st.sidebar.markdown("## 🏠 매물 리스트")
st.sidebar.markdown("---")

if not properties:
    st.sidebar.warning("표시할 매물이 없습니다.")
else:
    for prop in properties:
        # 각 매물을 테두리가 있는 컨테이너로 묶어 시각적으로 구분
        with st.sidebar.container(border=True):
            st.markdown(f"#### {prop['title']}")
            st.caption(f"{prop['address']}")
            
            col1, col2 = st.columns(2)
            col1.text(f"거래: {prop['transaction']}")
            col2.text(f"관리비: {prop['management_fee']}")

            col1, col2 = st.columns(2)
            col1.text(f"면적: {prop['area']}")
            col2.text(f"층/구조: {prop['floor']} / {prop['type']}")
            
            # 상세 정보는 펼치기/접기(expander)로 제공
            with st.expander("상세 정보 보기"):
                st.write(f"**방향:** {prop['direction']}")
                st.write(f"**난방/냉방:** {prop['heating']} / {prop['cooling']}")
                st.write(f"**생활시설:** {prop['living_facilities']}")
                st.write(f"**보안:** {prop['security']}")
                st.write(f"**기타:** {prop['etc']}")


# --- 메인 화면 (지도) ---
# 지도의 중앙 위치를 첫 번째 매물 위치로 설정 (데이터가 있을 경우)
map_center = [37.513083, 126.938559] # 기본값: 서울
if properties:
    map_center = [properties[0]['lat'], properties[0]['lon']]

m = folium.Map(location=map_center, zoom_start=15)

# 매물 데이터를 기반으로 마커 추가
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

# Streamlit에 지도 표시
st_folium(m, use_container_width=True, height=800)