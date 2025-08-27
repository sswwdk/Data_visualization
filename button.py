import streamlit as st

# CSS 스타일 정의 - 버튼 호버 시 노란색으로 변경
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ffffff;
    color: #000000;
    border: 2px solid #cccccc;
    border-radius: 5px;
    padding: 0.5rem 1rem;
    font-size: 16px;
    transition: all 0.3s ease;
}

div.stButton > button:first-child:hover {
    background-color: #ffff00 !important;
    color: #000000 !important;
    border-color: #cccc00 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

div.stButton > button:first-child:active {
    background-color: #e6e600 !important;
    transform: translateY(0px);
}
</style>
""", unsafe_allow_html=True)

# 페이지 제목
st.title("호버 효과가 있는 버튼들")

# 버튼 3개 생성
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("버튼 1"):
        st.success("버튼 1이 클릭되었습니다!")

with col2:
    if st.button("버튼 2"):
        st.success("버튼 2가 클릭되었습니다!")

with col3:
    if st.button("버튼 3"):
        st.success("버튼 3이 클릭되었습니다!")

# 추가 정보
st.markdown("---")
st.info("위의 버튼들에 마우스를 올려보세요. 노란색으로 변하는 호버 효과를 확인할 수 있습니다.")