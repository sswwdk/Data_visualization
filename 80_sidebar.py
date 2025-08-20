import streamlit as st
from PIL import Image
# sidebar. columns, tabs, expander

st.title('스트림릿 앱 페이지 구성하기')

st.sidebar.header('웰컴 메뉴')
selected_menu = st.sidebar.selectbox(
    '메뉴선택', ['메인','분석','설정']
)

# make_anal_tab() 함수 선언
def make_anal_tab():
    tab1, tab2, tab3 = st.tabs(['차트', '데이터', '설정'])
    with tab1:
        st.subheader('차트 탭')
        st.bar_chart({'데이터' : [1,2,3,4,5]})

    with tab2:
        st.subheader('데이터 탭')
        st.dataframe({'기준': ['a','b','c','d','e'], '값':[1,2,3,4,5]})

    # 3번쨰 설정 탭: 체크박스(활성화 여부), 슬라이더(업데이트 주기 sec)
    with tab3:
        st.subheader('체크박스')
        st.checkbox('자동 업데이트 활성화 여부')
        st.slider('업데이트 주기 (sec)', 0, 60, 30)


# st.columns(2)를 사용해 두 개의 컬럼을 생성합니다.
col1, col2 = st.columns(2)

if selected_menu == '메인':
    st.header('*메인 페이지*')
    st.write('환영합니다.!.!')
    img = Image.open('./data/image/image1.png')
    st.image(img, width=300, caption='Image from Unsplash')
elif selected_menu == '분석':
    st.header('*분석 페이지*')
    st.write('여기서 데이터를 선택 할 수 있습니다.')
    img = Image.open('./data/image/image3.png')
    st.image(img, width=300, caption='Image from Unsplash')
    make_anal_tab()
else:
    st.header('*설정 페이지*')
    st.write('앱 설정을 수정할 수 있습니다.')
    with col1:
        img = Image.open('./data/image/image4.png')
        st.image(img, width=300, caption='Image from Unsplash')
    with col2:
        img2 = Image.open('./data/image/image5.png')
        st.image(img2, width=300, caption='Image from Unsplash')

if st.sidebar.button('선택'):
    st.sidebar.write(f'{selected_menu} 페이지를 선택하셨습니다.')

# 슬라이드바 추가 0~100, 50
score = st.slider('슬라이드바', 0, 100, 50) # start, end, init_value

st.divider()

# tab 추가
st.header('탭 추가')
    
# 확장영역 추가
st.header('익스팬더 추가')
with st.expander('숨긴 영역'):
    st.write('여기는 보이지 않습니다. 클릭해야 보입니다.')