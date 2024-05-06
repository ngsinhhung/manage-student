from manage_student.model import *
from manage_student.utils import *


def get_teacher_not_presidential():
    teachers_is_president = db.session.query(Class.teacher_id).filter(Class.year == get_current_year())
    teachers_not_presidential = db.session.query(Teacher).filter(Teacher.id.not_in(teachers_is_president)).all()
    return teachers_not_presidential
