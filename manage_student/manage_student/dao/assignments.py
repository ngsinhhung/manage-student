from sqlalchemy.orm import joinedload

from manage_student import db
from manage_student.model import *
from manage_student.dao.teacher import *

def load_class_by_grade(grade):
    return Class.query.filter_by(grade=grade)

def load_subject_of_class(grade):
    return Subject.query.filter_by(grade=grade)


def load_all_teacher_subject(subject_id):
    return Teacher.query.join(Teachers_Subject).filter(Teachers_Subject.subject_id == subject_id).all()


def get_semester(semester_id):
    return db.session.get(Semester, semester_id)

def load_assignments_of_class(class_id):
    return Teaching_plan.query.filter_by(class_id=class_id)

def get_id_teacher_subject(teacher_id, subject_id):
    return Teachers_Subject.query.filter_by(teacher_id=teacher_id, subject_id=subject_id).first()

def save_subject_assignment(class_id, semester_id, teacher_subject_id):
    if isinstance(semester_id, int):
        plan, created = get_or_create(class_id=class_id, semester_id=semester_id, teacher_subject_id=teacher_subject_id)
        if created:
            plan.class_id = class_id
            plan.semester_id = semester_id
            plan.teacher_subject_id = teacher_subject_id
            db.session.commit()
        another = Teaching_plan.query.filter_by(class_id=class_id, semester_id=3 - semester_id,
                                                teacher_subject_id=teacher_subject_id).first()
        if another:
            db.session.delete(another)
            db.session.commit()

    else:
        for s in semester_id:
            plan, created = get_or_create(class_id=class_id, semester_id=s, teacher_subject_id=teacher_subject_id)
            if created:
                plan.class_id = class_id
                plan.semester_id = s
                plan.teacher_subject_id=teacher_subject_id
                db.session.commit()



def get_or_create(class_id, semester_id, teacher_subject_id):
    plan = Teaching_plan.query.filter_by(class_id=class_id, semester_id=semester_id, teacher_subject_id=teacher_subject_id).first()
    if plan:
        return plan, True
    else:
        create_plan = Teaching_plan(
            class_id=class_id,
            semester_id=semester_id,
            teacher_subject_id=teacher_subject_id
        )
        db.session.add(create_plan)
        db.session.commit()
        return create_plan, False



def delete_assignments(class_id):
    plans = Teaching_plan.query.filter_by(class_id=class_id)
    for plan in plans:
        db.session.delete(plan)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        for p in load_assignments_of_class(1):
            print(p.class_id, p.semester_id, p.teacher_subject.teacher_id, p.teacher_subject.subject_id)
