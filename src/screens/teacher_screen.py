import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_home

from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.database.db import create_teacher,check_teacher_exits, teacher_login


def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_register()




def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']}""")
        if st.button("Logout",type="secondary",key="loginbackbtn", shortcut="control+backspace", on_click=lambda: st.session_state.update({'login_type': None})):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1,tab2,tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type = type1, width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    
    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects',type = type2, width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    
    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attenddance_records' else "tertiary"
        if st.button('Attendance Records',type = type3, width='stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attenddance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == 'manage_subjects':
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == 'attenddance_records':
        teacher_tab_attendance_records()    


    footer_home()




def teacher_tab_take_attendance():
    st.header('Take AI Attendace!')

def teacher_tab_manage_subjects():
    st.header('Manage Subjects')


def teacher_tab_attendance_records():
    st.header('Attendance Records')




def login_teacher(teacher_username, teacher_pass):
    if not teacher_username or not teacher_pass:
        return False
    
    teacher = teacher_login(teacher_username,teacher_pass)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    
    return False




def teacher_screen_login():
    c1, c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.button(
            "Back",
            type="secondary",
            key="LoginBackButton",
            shortcut="control+backspace",
            on_click=lambda: st.session_state.update({'login_type': None, 'teacher_login_type': 'login'}),
        )

    st.header("Login", text_alignment="center")

    teacher_username = st.text_input("Enter Username", placeholder="name")
    st.markdown("<br>", unsafe_allow_html=True)
    teacher_password = st.text_input("Enter Password", type="password", placeholder="password")
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    
    
    btn1, btn2 = st.columns(2,vertical_alignment='center', gap='xxlarge')
    with btn1:
        if st.button("Login",type="secondary",key="LoginButton", shortcut="control+enter", width='stretch',icon=':material/passkey:'):
            if login_teacher(teacher_username,teacher_password):
                st.toast("Welcome Back!")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Username and Password combo")
        

    with btn2:
        if st.button("New Register",type="primary",key="RegisterButton",icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type = 'register'



    footer_home()






def register_teacher(teacher_username,teacher_name,teacher_password,teacher_pass_conform):
    if not teacher_username or not teacher_name or not teacher_password:
        return False, "All Fields are Requried!"
    if check_teacher_exits(teacher_username):
        return False, "Username Alreday Taken!"
    if teacher_password != teacher_pass_conform:
        return False, "Password Doesn't match!"
    
    try:
        create_teacher(teacher_username,teacher_password,teacher_name)
        return True, "Succesfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"


    


def teacher_screen_register():
    c1, c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.button(
            "Back",
            type="secondary",
            key="LoginBackButton",
            shortcut="control+backspace",
            on_click=lambda: st.session_state.update({'login_type': None, 'teacher_login_type': 'login'}),
        )
    
    st.header("Register For Teacher", text_alignment='center')
    teacher_username = st.text_input("Enter Username", placeholder="username")
    st.markdown("<br>", unsafe_allow_html=True)

    teacher_name = st.text_input("Enter Name", placeholder="name")
    st.markdown("<br>", unsafe_allow_html=True)

    teacher_password = st.text_input("Enter Password", type="password", placeholder="password")
    st.markdown("<br>", unsafe_allow_html=True)

    teacher_pass_conform = st.text_input("Conform Password", type='password', placeholder="password")
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()


    btn1, btn2 = st.columns(2,vertical_alignment='center', gap='xxlarge')
    with btn1:
        if st.button("Register Now",type="secondary", shortcut="control+enter", width='stretch',icon=':material/passkey:'):
            success, message = register_teacher(teacher_username,teacher_name,teacher_password,teacher_pass_conform)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with btn2:
        if st.button("Login Instead",type="primary",icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type = 'login'

    footer_home()
