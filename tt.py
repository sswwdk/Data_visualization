import streamlit as st

# 현재 열린 expander 저장
if "current_expander" not in st.session_state:
    st.session_state.current_expander = None

# expander 상태 토글 함수 (버튼 클릭 방식)
def set_expander_state(expander_key):
    if st.session_state.current_expander == expander_key:
        st.session_state.current_expander = None
    else:
        st.session_state.current_expander = expander_key

# 첫 번째 expander
with st.expander("첫 번째 Expander", expanded=st.session_state.current_expander == "expander1"):
    if st.button("첫 번째 열기/닫기"):
        set_expander_state("expander1")
    st.write("첫 번째 내용입니다.")

# 두 번째 expander
with st.expander("두 번째 Expander", expanded=st.session_state.current_expander == "expander2"):
    if st.button("두 번째 열기/닫기"):
        set_expander_state("expander2")
    st.write("두 번째 내용입니다.")
