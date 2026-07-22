import streamlit as st

from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_home
from PIL import Image
import numpy as np

def student_screen():

    style_background_dashboard()
    style_base_layout()

    c1, c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.button("Back",type="secondary",key="LoginBackButton", shortcut="control+backspace", on_click=lambda: st.session_state.update({'login_type': None}))

    st.header("Login using FaceID", text_alignment="center")

    photo_source = st.camera_input("Position Your Face in the center")

    if photo_source:
        np.array(Image.open(photo_source))


    footer_home()