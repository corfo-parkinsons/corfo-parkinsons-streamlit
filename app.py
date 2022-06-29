import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Dashboard Parkinsons",
        page_icon="👋",
        layout="wide"
    )

    st.write("# Parkinson Dash Streamlit! 👋")
    #st.write(str(pending))
    st.sidebar.success("Elige una demo.")

    st.markdown(
        """
        ### Pendientes
        - uno
        - dos
    """
    )


if __name__ == "__main__":
    run()
