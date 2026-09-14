import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_home
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.database.db import create_teacher, check_teacher_exits, teacher_login, get_teachers_subjects
from src.components.subject_card import subject_card
from src.components.dialog_add_photo import add_photos_dialog
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attendance
import numpy as np
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog


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
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendace!')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teachers_subjects(teacher_id)

    if not subjects:
        st.warning('You have not created any subjects yet! Please create one to begin!')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects }

    col1,col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_labels = st.selectbox('Select Subjects', options=list(subject_options.keys()))

    with col2:
        if st.button('Add photos',type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_labels]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Add Photos')
        gallary_cols = st.columns(4)

        for idx , img in enumerate(st.session_state.attendance_images):
            with gallary_cols[idx % 4]:
                st.image(img, width='stretch',caption=f'Photo {idx + 1}')
    has_photos = bool(st.session_state.attendance_images)
    c1,c2,c3 = st.columns(3)

    with c1:
        if st.button('Clear All Photos', width='stretch', type='tertiary', icon=':material/delete:',disabled= not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        
        if st.button('Run Face Analysis', type='secondary', width='stretch', icon=':material/analytics:', disabled= not has_photos):
            with st.spinner('Deep scanning classroom photos....'):
                all_detected_ids = {}

                for idx , img in enumerate(st.session_state.attendance_images): 
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _= predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id,[]).append(f'Photo {idx + 1}')

                enrolled_res = supabase.table('subject_students').select("*,student(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No student enrooled in this cource')
                else:

                    results , attendance_to_log = [] , []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['student']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id':  student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp':current_timestamp,
                            'is_present': bool(is_present)
                        })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)
    with c3:
        if st.button('Voice Atttendace', type='primary',width='stretch',icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)











def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1,col2 = st.columns(2)
    with col1:
        st.header("Manage Subjects")

    with col2:
        if st.button("Create new subject", width='stretch'):
            create_subject_dialog(teacher_id)

# showing all subjects

    subjects = get_teachers_subjects(teacher_id)
    if subjects:
        for subject_index, sub in enumerate(subjects):
            stats = [
                ("🙋🏻", "students", sub.get('total_students', 0)),
                ("🕰️", "classes", sub.get('total_classes', sub.get('total_class', 0))),
            ]

            def share_btn(sub=sub):
                subject_name = sub.get('name', 'Subject')
                subject_code = sub.get('subject_code') or sub.get('sub_code') or sub.get('code') or sub.get('sub_id') or ''
                subject_key = sub.get('subject_id', subject_index)
                if st.button(f"share Code: {subject_name}", key=f"share_{subject_code}_{subject_key}", icon=":material/share:"):
                    share_subject_dialog(subject_name, subject_code)
                st.space()

            subject_card(
                name=sub.get('name', 'Subject'),
                code=sub.get('subject_code') or sub.get('sub_code') or sub.get('code') or sub.get('sub_id') or '',
                section=sub.get('section', ''),
                stats=stats,
                footer_callback=share_btn,
            )
    else:
        st.info("No Subjects are Found. Create Above")




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
