import random

from manage_student.model import *
from manage_student.utils import *


def create_student(form):
    profile = Profile(name=form.full_name.data,
                      gender=int(form.gender.data),
                      birthday=form.birth_date.data,
                      address=form.address.data,
                      phone=form.phone_number.data,
                      email=form.email.data)
    db.session.add(profile)
    db.session.commit()
    student = Student(id=profile.id)
    db.session.add(student)
    db.session.commit()
    return student


def student_no_class(grade=None):
    student_had_class = db.session.query(Student.id).join(Students_Classes).join(Class).filter(
        Class.year == get_current_year())
    if grade:
        return db.session.query(Student).filter(Student.id.not_in(student_had_class)).filter(Student.grade == grade).all()
    return db.session.query(Student).filter(Student.id.not_in(student_had_class)).all()


def get_list_student_no_class_by_grade(size,grade):
    student_had_class = db.session.query(Student.id).join(Students_Classes).join(Class).filter(Class.year == get_current_year())
    non_class_students = db.session.query(Student).filter(Student.id.not_in(student_had_class)).filter(Student.grade == grade).all()
    return random.sample(non_class_students,size)


def get_student_by_id(id):
    return Student.query.get(id)


def check_student_in_class(student_id, class_id):
    return Students_Classes.query.filter(Students_Classes.student_id == student_id).filter(Students_Classes.class_id == class_id).first()


def view_score_student(student_id, semester_id):
    return (db.session.query(Subject.name, Score.type, Score.points, Exam.final_points)
            .join(Teaching_plan, Exam.teach_plan_id == Teaching_plan.id)
            .join(Score, Exam.id == Score.Exam_id)
            .join(Subject, Teaching_plan.subject_id == Subject.id)
            .filter(Exam.student_id == student_id)
            .filter(Teaching_plan.semester_id == semester_id)
            .all()
            )


def preprocess_scores(scores):
    subject_scores = {}
    for subject, exam_type, point, final_points in scores:
        if subject not in subject_scores:
            subject_scores[subject] = {'15_minute': [], '45_minute': [],'final_points' : ''}
        if exam_type == TYPEEXAM.EXAM_15P:
            subject_scores[subject]['15_minute'].append(point)
        elif exam_type == TYPEEXAM.EXAM_45P:
            subject_scores[subject]['45_minute'].append(point)
        subject_scores[subject]['final_points'] = final_points
    return subject_scores


if __name__ == '__main__':
    with app.app_context():
        print(view_score_student(4, 1))
