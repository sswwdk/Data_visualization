import os
import streamlit as st
from PIL import Image
import folium
from streamlit.components.v1 import html

st.title('방구 - 맞춤 방 구하기 서비스')

# ---------------- 세션 상태 초기화 ----------------
if "menu" not in st.session_state:
    st.session_state.menu = "방구 소개"
if "section" not in st.session_state:
    st.session_state.section = "기본 정보"

# selectbox/radio 변경 시 세션에 반영
def _sync_menu():
    st.session_state.menu = st.session_state.menu_select

def _sync_section():
    st.session_state.section = st.session_state.section_radio

# ------- 지도 원 표시 함수 -------
def draw_radius_circles(m, lat, lon, selected_km=None, custom_m=None):
    """
    folium 지도 m 위에 1/3/5km 기본 원(선택 강조)과 커스텀(m) 원을 그린다.
    """
    # 기본 반경 원
    options = [
        (1000,  "1 km"),
        (3000,  "3 km"),
        (5000,  "5 km"),
    ]
    highlight_radius = int(selected_km * 1000) if selected_km else None

    for r_m, label in options:
        folium.Circle(
            location=(lat, lon),
            radius=r_m,
            color="#007aff" if (highlight_radius == r_m) else "#5a8dee",
            weight=3 if (highlight_radius == r_m) else 1,
            fill=True,
            fill_opacity=0.12,
            tooltip=f"{label} 반경"
        ).add_to(m)

    # 커스텀 원
    if custom_m:
        folium.Circle(
            location=(lat, lon),
            radius=int(custom_m),
            color="#e74c3c",
            weight=4,
            fill=True,
            fill_opacity=0.10,
            tooltip=f"커스텀 반경: {int(custom_m)} m ({custom_m/1000:.2f} km)"
        ).add_to(m)

    # 중심 마커
    folium.Marker(
        location=(lat, lon),
        tooltip="중심 위치",
        popup=f"위도 {lat:.6f}, 경도 {lon:.6f}"
    ).add_to(m)

# ---------------- 사이드바: 메뉴/섹션 선택 + 완료 ----------------
st.sidebar.header('메뉴')
st.sidebar.selectbox(
    '메뉴선택',
    ['방구 소개', '방 찾기', '매물'],
    index=['방구 소개', '방 찾기', '매물'].index(st.session_state.menu),
    key='menu_select',
    on_change=_sync_menu
)

def sidebar_nav():
    st.sidebar.subheader("방 찾기")
    st.sidebar.radio(
        "필터",
        ['기본 정보', '예산', '방', '상세조건'],
        index=['기본 정보', '예산', '방', '상세조건'].index(st.session_state.section),
        key="section_radio",
        on_change=_sync_section
    )
    if st.sidebar.button("완료"):
        st.session_state.menu = "매물"
        st.rerun()

# ---------------- 매물(메인 영역) ----------------
def result():
    tab1, tab2, tab3 = st.tabs(['종합', '가격', '거리'])

    with tab1:
        st.subheader('종합필터 적용 결과')
        st.text('선택하신 필터를 종합적으로 봤을 때 가장 잘 맞는 매물입니다')
        for i in range(1, 5):
            with st.container(border=True):
                st.write(f"**매물 {i}: 선택한 지역 {i}순위로 반영**")
                st.write("매물의 특징: 거리가 가깝습니다!")
                st.write("배경: 방 사진")
                st.write("뜨는 정보: 지역, 평수, 방 개수, 보증금, 월세")

    with tab2:
        st.subheader('가격필터 적용 결과')
        st.text('선택하신 필터를 가격면에서 봤을 때 가장 잘 맞는 매물입니다')
        for i in range(1, 5):
            with st.container(border=True):
                st.write(f"**매물 {i}: 가격순 {i}위**")
                st.write("매물의 특징: 저렴합니다!")
                st.write("배경: 방 사진")
                st.write("뜨는 정보: 지역, 평수, 방 개수, 보증금, 월세")

    with tab3:
        st.subheader('거리필터 적용 결과')
        st.text('선택하신 필터를 거리 기준으로 봤을 때 가장 잘 맞는 매물입니다')
        for i in range(1, 5):
            with st.container(border=True):
                st.write(f"**매물 {i}: 선택한 지역 {i}순위로 반영**")
                st.write("매물의 특징: 거리가 가깝습니다!")
                st.write("배경: 방 사진")
                st.write("뜨는 정보: 지역, 평수, 방 개수, 보증금, 월세")

# ---------------- 페이지 라우팅 ----------------
if st.session_state.menu == '방구 소개':
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        img = Image.open('./raw.png')
        st.image(img, width=200, caption='방구 마스코트')
    st.write('방구에 대한 소개 - 방구는 무엇인가? 우리의 강점')

elif st.session_state.menu == '방 찾기':
    # 사이드바: 섹션 선택 & 완료 버튼
    sidebar_nav()

    # --- 메인: 섹션별 UI ---
    if st.session_state.section == '기본 정보':
        st.subheader('원하는 동네 기준 선택')

        check_work = st.checkbox('회사 근처가 좋아요', key="check_work_main")
        if check_work:
            work_input = st.text_input('회사 주소를 입력해주세요', key="work_input_main")
            st.caption(f'입력하신 회사 주소: {work_input or "-"}')

            st.markdown("##### 지도와 반경 (좌표 입력 후 '검색')")
            # 좌표 + 반경 입력 UI
            c1, c2 = st.columns(2)
            with c1:
                lat_str = st.text_input("위도", placeholder="37.5665", key="lat_input")
            with c2:
                lon_str = st.text_input("경도", placeholder="126.9780", key="lon_input")

            c3, c4 = st.columns(2)
            with c3:
                radius_label = st.radio("반경 선택", ["1 km", "3 km", "5 km"], index=0, horizontal=True)
                selected_km = int(radius_label.split()[0])
            with c4:
                custom_on = st.checkbox("커스텀 반경(m)")
            custom_m = st.slider("커스텀 반경(미터)", 200, 10000, 2000, 100) if custom_on else None

            # 검색 버튼
            if st.button("검색"):
                lat = lon = None
                error = None
                try:
                    lat = float(lat_str)
                    lon = float(lon_str)
                    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
                        error = "위도/경도 범위를 확인해주세요. (위도 -90~90, 경도 -180~180)"
                except Exception:
                    error = "위도/경도를 숫자로 입력해주세요. 예: 37.5665 / 126.9780"

                if error:
                    st.error(error)
                else:
                    # folium 지도 생성 및 원 그리기
                    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="CartoDB positron")
                    draw_radius_circles(
                        m,
                        lat,
                        lon,
                        selected_km=None if custom_on else selected_km,
                        custom_m=custom_m
                    )
                    # streamlit-folium 없이 HTML로 임베드
                    html(m.get_root().render(), height=520)

        check_town = st.checkbox('원하는 동네가 있어요', key="check_town_main")
        if check_town:
            town_input = st.text_input('원하는 동네를 입력해주세요', key="town_input_main")
            st.caption(f'입력하신 동네: {town_input or "-"}')

        st.divider()
        
        st.subheader('연령대 선택')
        st.selectbox('연령대를 선택하세요',
                     ['선택안함', '20대', '30대', '40대', '50대 이상'],
                     key="age_main")

    elif st.session_state.section == '예산':
        st.subheader('보증금 선택')
        min_deposit, max_deposit = st.slider(
            '원하는 보증금 범위 (만원)',
            min_value=0, max_value=10000, value=(50, 200), key="deposit"
        )
        st.caption(f'보증금: {min_deposit} ~ {max_deposit} 만원')

        st.divider()

        st.subheader('월세 선택')
        min_rent, max_rent = st.slider(
            '원하는 월세 범위 (만원)',
            min_value=0, max_value=200, value=(30, 50), key="rent"
        )
        st.caption(f'월세: {min_rent} ~ {max_rent} 만원')

    elif st.session_state.section == '방':
        st.subheader('평수 선택')
        min_size, max_size = st.slider(
            '원하는 평수 범위',
            min_value=0, max_value=200, value=(10, 30), key="size"
        )
        st.caption(f'평수: {min_size} ~ {max_size} 평')

        st.divider()

        st.subheader('방 개수 선택')
        st.selectbox(
            '방 개수를 선택하세요',
            ['상관없음', '1개', '2개', '3개', '4개', '5개 이상'],
            key="rooms"
        )

    elif st.session_state.section == '상세조건':
        st.subheader('상세필터 선택')
        filters = st.multiselect(
            '상세필터를 선택하세요',
            ['선택안함','주차 가능','관리비 없음','반려동물 가능','반지하 상관없음',
             '세탁기','건조기','에어컨','가스레인지','인덕션','엘리베이터'],
            key="filters"
        )
        st.caption(f'선택한 상세필터: {", ".join(filters) if filters else "-"}')

else:  
    st.subheader('매물')
    st.write('선택하신 필터에 따른 매물 리스트입니다!')
    result()
