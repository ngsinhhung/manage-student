from manage_student import db
from manage_student.model import *

def get_subject_by_id(subject_id):
    return db.session.get(Subject, subject_id)

