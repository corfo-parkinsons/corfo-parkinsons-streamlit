import streamlit as st
from streamlit.logger import get_logger
from aws import *

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Dashboard Parkinsons",
        page_icon="👋",
        layout="wide"
    )

    st.write("# Parkinson Dash Streamlit! 👋")
    st.image('logoCP.jpg', width=200)
    st.sidebar.success("Elige una página.")

    st.dataframe(schedule())

if __name__ == "__main__":
    run()
