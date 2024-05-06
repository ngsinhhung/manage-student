import datetime
from manage_student import db
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


if __name__ == '__main__':
    with app.app_context():
        for student in student_no_class():
            print(student.profile.name)
