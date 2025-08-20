import streamlit as st
st.title('스트림릿 안녕하세요')

st.write("오늘은 2025년 08월 18일 GD 생일이다. 하지만 오늘은 월요일이기도 하다. 힘들다. 나는 무엇을 위해 살아가는가...")
st.write("오늘은 2025년 08월 19일이다. 오늘은 화요일이다. 오늘 유독 집중이 안된다. 하지만 오늘도 끝냈다. 나는 무엇을 위해 살아가는가..." )
st.write("안녕하세요 스트림릿 당신은 누굽니까? 살아 있습니까? 이것도 아니라면 당신은 무엇입니까? 눈에 보이지 않지만 잘 부탁드립니다. 저는 사람 입니다. 당신을 다룹니다.")
st.write("오늘은 2025년 8월 20일. 수요일이다. 전날 술을 많이 마셔서 힘들다. 오전 10시 회복했다. 나는 무적이다.")

st.divider()

name = st.text_input("이름 : ")
if name: 
    st.write(f'안녕하세요. 저는 {name} 입니다. sssiiiuuuu')


import pandas as pd
df = pd.read_csv('./data/ABNB_stock.csv')
print(df)
df
