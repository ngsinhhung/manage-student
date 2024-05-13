import random

from sqlalchemy import extract

from manage_student.model import *
from manage_student.utils import *
from manage_student.utils import get_current_year

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


def get_all_semester():
    return Semester.query.all()

def verify_student_phone_number(phone_number):
    return db.session.query(Student.id, Profile.name).join(Profile).filter(Profile.phone == phone_number).first()



def view_score_student(student_id, semester_id):
    return (db.session.query(Exam, Subject.name, Score.type, Score.score,Score.count,extract('YEAR', Teaching_plan.score_deadline))
            .join(Teaching_plan, Exam.teach_plan_id == Teaching_plan.id)
            .join(Score, Exam.id == Score.Exam_id)
            .join(Subject, Teaching_plan.subject_id == Subject.id)
            .filter(Exam.student_id == student_id)
            .filter(Teaching_plan.semester_id == semester_id).filter(extract('YEAR', Teaching_plan.score_deadline) == get_current_year())
            .all()
            )


def preprocess_scores(scores):
    subject_scores = {}
    for exam, name, type, score, count,_ in scores:
        if name not in subject_scores:
            subject_scores[name] = {'15_minute': {'scores': [], 'count': 0}, '45_minute': {'scores': [], 'count': 0},
                                    'final_points': {'scores': [], 'count': 0}}

        if type == TYPEEXAM.EXAM_15P:
            subject_scores[name]['15_minute']['scores'].append(score)
        elif type == TYPEEXAM.EXAM_45P:
            subject_scores[name]['45_minute']['scores'].append(score)
        elif type == TYPEEXAM.EXAM_final:
            subject_scores[name]['final_points']['scores'].append(score)
    return subject_scores


if __name__ == '__main__':
    with app.app_context():
        # print(verify_student_phone_number(1000000000))
        print(view_score_student(4, 1))
