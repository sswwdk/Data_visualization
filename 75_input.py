import streamlit as st

st.title('Title')
st.header('Header')
st.subheader('SubHeader')

st.write('하이로 나는 한로로 노래가 좋아')
st.text('하이로 나는 한로로 노래가 좋아')

st.markdown(
    '''
    여기는 메인 텍스트 입니다.
    :red[Red], :blue[Blue], :green[Green.]\n
    **ZZaSS** ZZaSS\n
    *이탤릭체*로 표현 할 수 있어요
            
    '''
)

st.code(
    '''
    st.title('Title')
    st.header('Header')
    st.subheader('SubHeader')
    ''', language='html'
)

st.divider()

# st.button('hello', icon='👴') # secondary type
# st.button('hello', type='primary')
# st.button('hello', type='primary', disabled=True, key=2) # disabled 클릭 X


st.button('Reset', type='primary') # 리셋이 되는게 아니라 누르면 화면이 갱신되어 안보이게 된 것

def button_write():
    st.write('버튼이 클릭되었습니다!')

st.button('activate', on_click=button_write)

st.divider()

clicked = st.button('activate2', type='primary')
if clicked:
    st.write(' 버튼2개가 클릭되었습니다. ')

####################################
st.header('같은 버튼 여러개 만들기')

# key =
# activate button 5개 primary

for i in range(1,6):
    clicked = st.button('activate',type='primary', key=f'act_btn_{i}')


####################################