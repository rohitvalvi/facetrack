import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time

@st.dialog("Enroll in Subject")
def enroll_dialog(student_id):
    st.write('Enter the Subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject_Code', placeholder="eg. CS101")

    if st.button('Enroll Now', key='manual_enroll_confirm', type='primary',width='stretch'):
        if join_code:
            res = supabase.table('subjects').select('subject_id,name,subject_code').eq('subject_code', join_code).execute()
            if res.data:
                subject = res.data[0]

                check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id',student_id).execute()
                if check.data:
                    st.warning('You have already Enroll for this program')
                else:
                    enroll_student_to_subject(student_id,subject['subject_id'])
                    st.success('Succesfully Enrolled!')
                    time.sleep(1)
                    st.rerun()
        else:
            st.warning('Please Enter a subject code')