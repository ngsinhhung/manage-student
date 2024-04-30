
from manage_student.model import *

def create_student(form):
    profile = Profile(name=form.full_name.data,
                      gender=int(form.gender.data),
                      dob=form.birth_date.data,
                      address=form.address.data,
                      phone=form.phone_number.data,
                      email=form.email.data)
    db.session.add(profile)
    db.session.commit()
    student = Student(id=profile.id)
    db.session.add(student)
    db.session.commit()
    return student


def student_no_class():
    student_had_class = db.session.query(Student.id).join(Students_Classes).join(Class).filter(Class.year == 2024).all()
    non_class_students = db.session.query(Student).filter(Student.id.not_in(student_had_class)).all()
    return non_class_students




if __name__ == '__main__':
    with app.app_context():
        for student in student_no_class():
            print(student.profile.name)
