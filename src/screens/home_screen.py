import streamlit as st


from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_background_home, style_base_layout

def home_screen():
    header_home()
    

    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("src/assets/studentLogo.png", width=120)
        if st.button('Student Portal', use_container_width=True, type="primary",icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()         

    with col2:
        st.header("I'm Teacher")
        st.image("src/assets/teacherLogo.png", width=120)
        if st.button('Teacher Portal', use_container_width=True, type="primary", icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()
        
