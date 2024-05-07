from manage_student import db
from manage_student.model import *
from manage_student.dao.teacher import *

def load_class_by_grade(grade):
    return Class.query.filter_by(grade=grade)

def load_subject_of_class(grade):
    return Subject.query.filter_by(grade=grade)

def add_assignments_of_class(teacher_id, class_id, semester_id, subject_id):
    teacher_plan = Teaching_plan(
        teacher_id=db.session.get(Teacher, teacher_id).id,
        class_id=db.session.get(Class, class_id).id,
        semester_id=db.session.get(Semester, semester_id),
        subject_id=db.session.get(Subject, subject_id),
    )
    db.session.add(teacher_plan)
    db.session.commit()


def load_assignments_of_class(classname):
    pass

if __name__ == '__main__':
    with app.app_context():
        pass