from manage_student import db
from manage_student.model import *
from manage_student.dao.teacher import *

def load_class_by_grade(grade):
    return Class.query.filter_by(grade=grade)

def load_subject_of_class(grade):
    return Subject.query.filter_by(grade=grade)

def save_subject_assignment(teacher_id, class_id, semester_id, subject_id):
    for seme in semester_id:
        plan, created = get_or_create(teacher_id=teacher_id, class_id=class_id, semester_id=seme, subject_id=subject_id)
        if created:
            plan.teacher_id = teacher_id
            plan.class_id = class_id
            plan.semester_id = seme
            plan.subject_id = subject_id
            another = Teaching_plan.query.filter_by(class_id=class_id, semester_id=3-seme, subject_id=subject_id).first()
            if another:
                db.session.delete(another)
            db.session.commit()

def get_or_create(teacher_id, class_id, semester_id, subject_id):
    plan = Teaching_plan.query.filter_by(class_id=class_id, semester_id=semester_id, subject_id=subject_id).first()
    if plan:
        return plan, True
    else:
        create_plan = Teaching_plan(
            teacher_id=db.session.get(Teacher, teacher_id).id,
            class_id=db.session.get(Class, class_id).id,
            semester_id=db.session.get(Semester, semester_id).id,
            subject_id=db.session.get(Subject, subject_id).id,
        )
        db.session.add(create_plan)
        db.session.commit()
        return create_plan, False
def get_semester(semester_id):
    return db.session.get(Semester, semester_id)
def load_assignments_of_class(class_id):
    return Teaching_plan.query.filter_by(class_id=class_id)

def delete_assignments(class_id):
    plans = Teaching_plan.query.filter_by(class_id=class_id)
    for plan in plans:
        db.session.delete(plan)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        pass
