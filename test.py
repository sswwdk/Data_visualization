import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("CSV 파일 업로드 & 동적 그래프 시각화")

# 1. 파일 업로드
file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if file is not None:
    # 2. 데이터 불러오기
    df = pd.read_csv(file)
    st.write("### 데이터 미리보기")
    st.dataframe(df)

    # 3. 컬럼 선택
    columns = df.columns.tolist()
    x_axis = st.selectbox("X축 컬럼 선택", options=columns)
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    y_axis = st.selectbox("Y축 컬럼 선택 (수치형)", options=numeric_cols)

    # 4. X축이 날짜형이면 단위 선택 옵션 제공
    # 원본 데이터프레임의 복사본을 만들어 날짜 변환을 시도합니다.
    df_copy = df.copy()
    try:
        df_copy[x_axis] = pd.to_datetime(df_copy[x_axis])
    except Exception:
        pass

    if pd.api.types.is_datetime64_any_dtype(df_copy[x_axis]):
        st.info(f"'{x_axis}' 컬럼은 날짜 데이터로 인식되었습니다.")
        group_option = st.radio("날짜 단위 선택", ["일", "월", "연"], horizontal=True)

        if group_option == "일":
            df["X_axis_grouped"] = df_copy[x_axis].dt.strftime('%Y-%m-%d')
        elif group_option == "월":
            df["X_axis_grouped"] = df_copy[x_axis].dt.to_period('M').astype(str)
        else:  # 연 단위
            df["X_axis_grouped"] = df_copy[x_axis].dt.to_period('Y').astype(str)

        x_axis_display = "X_axis_grouped" # 그룹화된 컬럼으로 교체
    else:
        x_axis_display = x_axis # 원본 컬럼 사용

    # 5. Y축 값 보정 옵션 (로그/제곱근)
    scale_option = st.radio("Y축 스케일링 방법", ["원본", "로그 변환", "제곱근 변환"], horizontal=True)

    if scale_option == "로그 변환":
        df["Y_axis_scaled"] = np.log1p(df[y_axis])  # log(1+x)
        y_axis_label = f"log(1+{y_axis})"
    elif scale_option == "제곱근 변환":
        df["Y_axis_scaled"] = np.sqrt(df[y_axis].clip(lower=0))  # 음수 방지
        y_axis_label = f"sqrt({y_axis})"
    else:
        df["Y_axis_scaled"] = df[y_axis]
        y_axis_label = y_axis

    # 6. 그래프 종류 선택
    chart_type = st.radio("그래프 종류 선택", options=["Box Plot", "Scatter", "Bar"], horizontal=True)

    # 7. 그래프 생성
    # y축에 표시될 이름을 y_axis_label 변수로 지정합니다.
    labels = {x_axis_display: x_axis, "Y_axis_scaled": y_axis_label}

    if chart_type == "Box Plot":
        fig = px.box(df, x=x_axis_display, y="Y_axis_scaled", title=f"Box Plot: {y_axis_label} by {x_axis}", labels=labels)
    elif chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis_display, y="Y_axis_scaled", title=f"Scatter Plot: {y_axis_label} vs {x_axis}", labels=labels)
    elif chart_type == "Bar":
        # Bar 차트는 집계가 필요할 수 있으므로, 여기서는 평균값을 사용합니다.
        # 사용 사례에 맞게 sum(), count() 등으로 변경할 수 있습니다.
        grouped_df = df.groupby(x_axis_display)["Y_axis_scaled"].mean().reset_index()
        fig = px.bar(grouped_df, x=x_axis_display, y="Y_axis_scaled", title=f"Bar Plot: {y_axis_label} by {x_axis}", labels=labels)

    # 8. Streamlit에 표시
    st.plotly_chart(fig, use_container_width=True)

###############################################################
st.divider()
###############################################################

st.title('Tips Data')
df = sns.load_dataset('tips')

# 위젯을 활용한 interactive 그래프 표현
x_options = ['day','size']
y_options = ['total_bill','tip']
hue_options = ['smoker','sex']

x_option = st.selectbox(
    'Select X-axis',
    index=None,
    options=x_options
)

y_option = st.selectbox(
    'Select Y-axis',
    index=None,
    options=y_options
)

hue_option = st.selectbox(
    'Select Hue',
    index=None,
    options=hue_options
)

if (x_option != None) & (y_option != None):
    if hue_option != None:
        fig3 = px.box(
            data_frame=df, x=x_option, y=y_option,
            color=hue_option, width=500
        )
    else:
        fig3 = px.box(
            data_frame=df, x=x_option, y=y_option,
            width=500
        )
    st.plotly_chart(fig3)