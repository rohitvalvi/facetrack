from src.database.config import supabase

import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
    return bcrypt.hashpw(pwd.encode(), hashed.encode())

def check_teacher_exits(username):
    response = supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
    data = {"username": username, "password": hash_pass(password), "name": name }
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username,password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
        
    return None

def get_all_students():
    response = supabase.table("student").select("*").execute()

    return response.data


def create_student(new_name,face_embedding=None,voice_embedding=None):
    data = {'name': new_name, 'face_embedding': face_embedding, 'voice_embedding': voice_embedding}
    response = supabase.table("student").insert(data).execute()
    return response.data

def create_subject(sub_code, sub_name, section, teacher_id):
    payloads = [
        {"sub_code": sub_code, "name": sub_name, "section": section, "teacher_id": teacher_id},
        {"code": sub_code, "name": sub_name, "section": section, "teacher_id": teacher_id},
        {"sub_id": sub_code, "name": sub_name, "section": section, "teacher_id": teacher_id},
        {"subject_code": sub_code, "name": sub_name, "section": section, "teacher_id": teacher_id},
        {"name": sub_name, "section": section, "teacher_id": teacher_id},
    ]

    last_error = None
    for data in payloads:
        try:
            response = supabase.table("subjects").insert(data).execute()
            return response.data
        except Exception as exc:
            last_error = exc
            message = str(exc).lower()
            if "column" in message and "could not find" in message:
                continue
            raise

    raise last_error

# Backward-compatible alias used by older code.
def create_subjects(sub_code, sub_id, section, teacher_id):
    return create_subject(sub_code, sub_id, section, teacher_id)


def get_teachers_subjects(teacher_id):
    response = supabase.table("subjects").select("*, subject_students(count),attendance_log(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data or []

    for sub in subjects:
        subject_code = (
            sub.get("sub_code")
            or sub.get("code")
            or sub.get("sub_id")
            or sub.get("subject_code")
            or ""
        )
        sub['subject_code'] = subject_code
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_log', [])
        unique_session = len(set(log['timestamp'] for log in attendance if log.get('timestamp')))
        sub['total_classes'] = unique_session
        sub['total_class'] = unique_session

        sub.pop('subject_students', None)
        sub.pop('attendance_log', None)

    return subjects


def get_teacher_subjects(teacher_id):
    return get_teachers_subjects(teacher_id)

