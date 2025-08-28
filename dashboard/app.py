import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
import requests # GeoJSON 데이터를 URL에서 직접 로드하기 위해 추가
import numpy as np # 범례 구간 계산을 위해 numpy 추가

# 페이지 레이아웃을 'wide'로 설정하여 넓게 표시합니다.
st.set_page_config(layout="wide")
st.title("서울시 자치구별 연도별 범죄 데이터 시각화 🗺️")

# --- 데이터 로드 ---

# 1. 서울시 자치구 경계 GeoJSON 데이터 URL
seoul_geojson_url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json"

# 2. 'crime2.csv' 파일 로드
# 파일이 streamlit 앱 파일과 같은 디렉토리에 있어야 합니다.
try:
    df_year = pd.read_csv('data/crime2.csv')
except FileNotFoundError:
    st.error("'crime2.csv' 파일을 찾을 수 없습니다. 앱 파일과 같은 디렉토리에 업로드해주세요.")
    st.stop() # 파일이 없으면 앱 실행 중지

# --- 메인 화면 설정 (연도 및 색상 선택) ---

# 데이터프레임의 컬럼에서 연도 목록을 추출합니다. ('자치구별' 제외)
year_list = df_year.columns[1:].tolist()

# 사용 가능한 색상 맵 리스트 (낮은 값=초록, 높은 값=빨강을 위해 RdYlGn_r 추가)
color_map_list = ['RdYlGn_r', 'YlOrRd', 'YlGnBu', 'BuPu', 'GnBu', 'PuRd', 'RdPu', 'OrRd', 'BuGn', 'YlGn']


# st.columns를 사용하여 선택 박스를 가로로 나란히 배치합니다.
col1, col2 = st.columns([1, 1])

with col1:
    # 연도를 선택할 수 있는 selectbox를 생성합니다.
    selected_year = st.selectbox(
        '확인하고 싶은 연도를 선택하세요',
        year_list,
        index=len(year_list) - 1 # 가장 최근 연도를 기본값으로 선택
    )

with col2:
    # 히트맵 색상을 선택할 수 있는 selectbox를 생성합니다.
    # 기본값을 'RdYlGn_r'로 설정하여 낮은 값은 초록색, 높은 값은 빨간색으로 표시
    default_color_index = color_map_list.index('RdYlGn_r')
    selected_color = st.selectbox(
        '히트맵 색상을 선택하세요',
        color_map_list,
        index=default_color_index
    )


# --- 메인 화면 (지도 표시) ---

st.markdown(f"### 📍 **{selected_year}** 서울시 자치구별 범죄 데이터")

# 서울 중심부의 위도, 경도로 기본 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11,
    tiles="cartodbpositron", # 지도 타일 스타일 설정
    # 지도 조작 옵션 비활성화
    zoom_control=False,
    scrollWheelZoom=False,
    dragging=False
)

# --- 범례(Legend)를 위한 bins 계산 (오류 수정) ---
min_val = df_year[selected_year].min()
max_val = df_year[selected_year].max()

# 데이터 범위를 포함하는 깔끔한 시작/끝 값 계산 (천 단위)
start_bin = int(np.floor(min_val / 1000) * 1000)
end_bin = int(np.ceil(max_val / 1000) * 1000)

# 5~7개 사이의 적절한 구간 생성
num_bins = max(5, min(7, (end_bin - start_bin) // 1000 + 1))
bins = list(np.linspace(start_bin, end_bin, num=num_bins, dtype=int))

# 만약 데이터 편차가 너무 작아 구간이 3개 미만이면 100단위로 재계산
if len(set(bins)) < 3:
    start_bin = int(np.floor(min_val / 100) * 100)
    end_bin = int(np.ceil(max_val / 100) * 100)
    num_bins = max(5, min(7, (end_bin - start_bin) // 100 + 1))
    bins = list(np.linspace(start_bin, end_bin, num=num_bins, dtype=int))

final_bins = sorted(list(set(bins))) # 중복 제거 및 정렬


# Choropleth (단계 구분도) 레이어 추가
folium.Choropleth(
    geo_data=seoul_geojson_url,
    data=df_year,
    columns=['자치구별', selected_year],
    key_on='feature.properties.name',
    fill_color=selected_color,
    fill_opacity=0.8,
    line_opacity=0.3,
    legend_name=f'{selected_year} 범죄 발생 건수',
    bins=final_bins # 계산된 bins를 적용하여 범례를 깔끔하게 만듭니다.
).add_to(m)


# --- 지도에 자치구 이름과 반올림된 값 표시 ---

# URL에서 GeoJSON 데이터를 직접 로드하여 파이썬 객체로 변환
geo_data = requests.get(seoul_geojson_url).json()

# 표시할 데이터 (자치구별 범죄 건수)
crime_data = df_year.set_index('자치구별')[selected_year].to_dict()

# GeoJSON 데이터를 사용하여 각 자치구의 중심점을 계산하고 이름과 값을 표시합니다.
for feature in geo_data['features']:
    gu_name = feature['properties']['name']
    
    # 해당 자치구의 범죄 건수 가져오기
    value = crime_data.get(gu_name, 0)
    # 값을 백의 자리로 반올림 (10의 자리에서 반올림)
    rounded_value = int(round(value, -2))

    # 자치구의 중심점(centroid)을 간단히 계산합니다.
    coords = feature['geometry']['coordinates']
    
    # MultiPolygon의 경우, 가장 큰 폴리곤의 중심점을 사용합니다.
    if feature['geometry']['type'] == 'MultiPolygon':
        largest_polygon = max(coords, key=lambda polygon: len(polygon[0]))
        coords = largest_polygon

    lon, lat = zip(*coords[0])
    centroid = [sum(lat) / len(lat), sum(lon) / len(lon)]

    # folium.Marker와 DivIcon을 사용하여 텍스트 라벨을 추가합니다.
    # 자치구 이름과 반올림된 값을 함께 표시합니다.
    folium.Marker(
        location=centroid,
        icon=folium.DivIcon(
            icon_size=(150,40), # 아이콘 크기 높이 조절
            icon_anchor=(75,20), # 아이콘 앵커 조절
            html=f'<div style="font-size: 9pt; font-weight: bold; color: #333; text-align: center; width: 150px; text-shadow: -1px 0 white, 0 1px white, 1px 0 white, 0 -1px white;">{gu_name}<br>{rounded_value:,}</div>',
        )
    ).add_to(m)


# Streamlit 앱에 Folium 지도를 표시합니다.
st_folium(m, use_container_width=True, height=600)

# --- 데이터 테이블 표시 ---
# '자치구별' 컬럼을 인덱스로 설정하여 테이블을 더 깔끔하게 표시합니다.
df_years = df_year.set_index('자치구별')
st.markdown("---")
st.markdown("### 원본 데이터")
st.dataframe(df_years)