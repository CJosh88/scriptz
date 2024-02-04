import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import time 
if 'stage' not in st.session_state:
    st.session_state.stage = 4

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
    'Get Help': 'https://www.iqbusiness.net/ai-lab',
    'Report a bug': "https://www.iqbusiness.net/ai-lab"
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

def set_state(i):
    st.session_state.stage = i

returnHome = st.button('Click here to go back to the homepage', on_click=set_state(0))

if returnHome:
    switch_page('Home')