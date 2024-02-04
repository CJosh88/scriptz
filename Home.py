import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="AiRecruit Homepage",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
    'Get Help': 'https://www.iqbusiness.net/ai-lab',
    'Report a bug': "https://www.iqbusiness.net/ai-lab",
    'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Welcome to AiRecruit")
st.divider()

if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_state(i):
    st.session_state.stage = i

if st.session_state.stage == 0:

    #st.button('Begin', on_click=set_state, args=[1])

    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        b1 = st.button('Create new CV-scoring pipeline',on_click=set_state, args=[1])
    with col2:
        b2 = st.button('View existing pipelines',on_click=set_state, args=[5])

if st.session_state.stage == 1:
    switch_page('CreateNew')