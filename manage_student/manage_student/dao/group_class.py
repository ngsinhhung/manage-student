from manage_student.model import *
from manage_student import utils
from manage_student.dao import student


def get_class():
    return db.session.query(Class).join(Teacher).filter(Class.year == utils.get_current_year()).all()


def count_class():
    return Class.query.filter(Class.year == utils.get_current_year()).count()


def create_class(form):
    new_class = Class(grade=form.grade.data,
                      year=utils.get_current_year(),
                      count=count_class()+1,
                      teacher_id=form.teacher.data)
    db.session.add(new_class)
    db.session.commit()
    temp_student = student.get_list_student_no_class_by_grade(form.class_size.data,form.grade.data)
    for s in temp_student:
        student_class = Students_Classes(student_id=s.id,class_id=new_class.id)
        db.session.add(student_class)
        db.session.commit()


def get_info_class_by_name(grade,count):
    return Class.query.filter_by(grade="K"+str(grade), count=count).first()


if __name__ == '__main__':
    with app.app_context():
        for s in get_info_class_by_name(10,1).students:
            print(s.student)
