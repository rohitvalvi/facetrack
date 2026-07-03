import streamlit as st

from src.ui.base_layout import style_background_dashboard,style_base_layout


def student_screen():

    style_background_dashboard()
    style_base_layout()

    st.header('Student screen')