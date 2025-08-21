import streamlit as st

# layout 요소
# columns 는 요소를 왼쪽 -> 오른쪽으로 배치할 수 있다.

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        '오늘 날씨',
        value='35도'
    )

with col2:
    st.metric(
        '오늘 미세먼지',
        value='야르',
        delta='-30',
        delta_color='inverse'
    )

with col3:
    st.metric(
        '오늘 습도',
        value='습함'
    )

##
st.markdown('---')

data = {
    '이름' : ['홍길동', '김길동', '박길동'],
    '나이' : [10,20,30]
}

import pandas as pd
df = pd.DataFrame(data)
st.dataframe(df)

st.divider()

st.table(df)

st.json(data)

# datafile.csv >> load >> table 출력 >> px.box() > st.plotly_chart()
import pandas as pd
import plotly.express as px

st.title("CSV 파일 업로드 & Box Plot 시각화")

# 1. 파일 업로드
file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if file is not None:
    # 2. 데이터 불러오기
    df = pd.read_csv(file)
    st.write("### 데이터 미리보기")
    indata = st.dataframe(df)

    # 3. 박스플롯 생성 (X='Date', Y='Close')
    if indata:
        fig = px.box(data_frame=df, x='Cylinders', y='CO2 Emissions(g/km)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("안돼")


st.divider()

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("CSV 파일 업로드 & 동적 그래프 선택")

# 1. 파일 업로드
file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if file is not None:
    # 데이터 불러오기
    df = pd.read_csv(file)
    st.write("### 데이터 미리보기")
    st.dataframe(df)

    # 2. 컬럼 선택
    columns = df.columns.tolist()
    x_axis = st.selectbox("X축 컬럼 선택", options=columns)
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    y_axis = st.selectbox("Y축 컬럼 선택 (수치형)", options=numeric_cols)

    # 3. 그래프 종류 선택
    chart_type = st.radio("그래프 종류 선택", options=["Box Plot", "Scatter", "Bar"])

    # 4. 그래프 생성
    if chart_type == "Box Plot":
        # X축이 연속형이면 문자열로 변환해서 범주형 처리
        if pd.api.types.is_numeric_dtype(df[x_axis]) or pd.api.types.is_datetime64_any_dtype(df[x_axis]):
            df[x_axis] = df[x_axis].astype(str)
        fig = px.box(df, x=x_axis, y=y_axis, title=f"Box Plot: {y_axis} by {x_axis}")
    elif chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot: {y_axis} vs {x_axis}")
    elif chart_type == "Bar":
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"Bar Plot: {y_axis} by {x_axis}")

    # 5. Streamlit에 표시
    st.plotly_chart(fig, use_container_width=True)

