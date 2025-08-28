import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# --- 데이터 처리 ---
# 1. 로컬 CSV 파일 읽기
try:
    # 'crime.csv' 파일이 스크립트와 같은 경로에 있다고 가정합니다.
    # 한글 깨짐 방지를 위해 encoding='utf-8' 또는 'cp949'를 사용합니다.
    file_path = 'crime.csv'
    df = pd.read_csv(
        file_path, 
        skiprows=5,  # 데이터 앞부분의 불필요한 5줄 건너뛰기
        header=None, # 파일에 헤더(컬럼명)가 없으므로 None으로 설정
        names=['구분', '구', '발생건수'], # 데이터프레임의 열 이름 지정
        encoding='utf-8'
    )

    # 2. Plotly Express로 막대 차트 생성
    fig = px.bar(
        df,
        x='구',
        y='발생건수',
        title='2023년 서울시 자치구별 범죄 발생 건수',
        labels={'구': '자치구', '발생건수': '발생 건수'},
        text='발생건수'  # 막대 위에 수치 표시
    )

    # 차트 레이아웃 꾸미기
    fig.update_traces(textposition='outside') # 텍스트를 막대 바깥쪽에 표시
    fig.update_layout(
        xaxis_tickangle=-45, # x축 레이블이 겹치지 않도록 45도 회전
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    
    # 그래프를 담을 컴포넌트 생성
    graph_component = dcc.Graph(
        id='crime-bar-chart',
        figure=fig
    )

except FileNotFoundError:
    # 파일을 찾지 못했을 경우 에러 메시지 표시
    graph_component = html.Div([
        html.H3("오류: 'crime.csv' 파일을 찾을 수 없습니다.", style={'color': 'red'}),
        html.P("파이썬 스크립트와 동일한 폴더에 'crime.csv' 파일이 있는지 확인해주세요.")
    ])
except Exception as e:
    # 그 외 다른 오류 발생 시 메시지 표시
    graph_component = html.Div([
        html.H3("오류: 데이터를 처리하는 중 문제가 발생했습니다.", style={'color': 'red'}),
        html.P(f"에러 내용: {e}")
    ])


# --- Dash 앱 설정 ---
# 3. Dash 앱 초기화
app = dash.Dash(__name__)

# 4. 앱 레이아웃 정의
app.layout = html.Div(children=[
    html.H1(children='서울시 자치구별 범죄 현황 대시보드'),

    html.Div(children='''
        'crime.csv' 파일의 데이터를 기반으로 생성된 차트입니다.
    '''),

    # 위에서 생성한 그래프 또는 에러 메시지 컴포넌트를 여기에 배치
    graph_component
])

# 5. 앱 실행
if __name__ == '__main__':
    app.run(debug=True)