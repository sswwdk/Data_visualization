import streamlit as st

# checkbox
check = st.checkbox('I agree')
if check:
    st.text('Welcome...!')
    #st.write('checkcheck')

# 함수, on_change = checkbox_write
    

def checkbox_write():
    st.write("체크박스가 클릭되었습니다!")

st.checkbox("check", on_change=checkbox_write)

st.divider()

## 세션-상태 값에 저장
if 'checkbox_state' not in st.session_state:
    st.session_state.checkbox_state = False

def checkbox_write1():
    st.session_state.checkbox_state = True

if st.session_state.checkbox_state:
    st.write('응...')

st.checkbox('진짜 죽을래???', on_change=checkbox_write1)

st.divider()

# 토글 버튼
selected = st.toggle('Turn on the switch!!')
if selected:
    st.text('Turn on!')
else:
    st.text('Turn off!')

st.divider()

#  selectbox 선택지
option = st.selectbox(
    '점심메뉴 고르기',
    options = ['김밥','떡볶이','우동','쫄면'],
    index=None,
    placeholder='네 개 중 하나만 골라야 돼'
)

st.text(f'오늘의 점심메뉴는 : {option}')

st.divider()

# radio
genre = st.radio(
    '무슨 영화를 좋아하세요?', ['멜로','스릴러','판타지'],
    captions =['봄날은 간다','트리거','원즈데이']
)
st.text(f'당신이 좋아하는 장르는 {genre}')

st.divider()

# multiselect
menus = st.multiselect(
    '먹고 싶은 것 다 골라', ['김밥','떡볶이','우동','쫄면']
)
st.text(f'내가 선택한 메뉴는 {menus}')

st.divider()

# slider
score = st.slider('내 점수 선택', 0, 100, 51) # start, end, init_value
st.text(f'score: {score}')

from datetime import time
st_time, end_time = st.slider(
    '공부시간 선택',
    min_value = time(0), max_value=time(11),
    value=(time(8), time(18)),
    format='HH:mm'
)
st.text(f'공부시간:{st_time} ~ {end_time}')

st.divider()

# text_input
tx1 = st.text_input('영화제목', placeholder ='제목을 입력하세요')
tx2 = st.text_input('비밀번호', placeholder ='비밀번호를 입력하세연', type='password')
st.text(f'텍스트 입력 결과 : {tx1}, {tx2}')

st.divider()

# 파일 업로더
# 업로드한 파일은 사용자의 세션에 있다. 화면 갱신하면 사라진다.
import pandas as pd

file = st.file_uploader(
    '파일 선택', type='csv', accept_multiple_files = False
)
# 파일 저장

if file is not None:
    df = pd.read_csv(file)
    st.write(df)

    with open(file.name, 'wb') as out:
        out.write(file.getbuffer())