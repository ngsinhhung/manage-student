from manage_student.model import *

def load_all_teachers():
    return Teacher.query.all()
    # return db.session.query(Profile).join(Teacher, Profile.id == Teacher.id).all()