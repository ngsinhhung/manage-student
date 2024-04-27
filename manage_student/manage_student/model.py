from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from manage_student import db,app
import enum


class UserRole(enum.Enum):
    STAFF = 1
    TEACHER = 2
    ADMIN = 3


class Title(enum.Enum):
    BACHELOR = 1
    MASTER = 2
    DOCTOR = 3


class GRADE(enum.Enum):
    K10 = 1
    K11 = 2
    K12 = 3


class TYPEEXAM(enum.Enum):
    EXAM_15P = 1
    EXAM_45P = 2


class Semester(db.Model):
    id = Column(Integer, primary_key=True,autoincrement=True)
    semester_name = Column(String(50))


class Profile(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    dob = Column(DateTime)
    gender = Column(Boolean)
    address = Column(Text)
    phone = Column(String(10), unique=True)


class User(db.Model, UserMixin):
    id = Column(Integer, ForeignKey(Profile.id), primary_key=True, nullable=False, unique=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    user_role = Column(Enum(UserRole))
    notifications = relationship("Notification", backref="user", lazy=True)

    def __str__(self):
        return self.name


class Staff(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True, nullable=False)


class Teacher(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True, nullable=False)
    title = Column(Enum(Title))

    class_teach = relationship("Class", backref="class_teach", lazy=True)


class Notification(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    noi_dung = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)


class Class(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    grade = Column(Enum(GRADE))
    count = Column(Integer)
    amount = Column(Integer, default=0)
    teacher_id = Column(Integer, ForeignKey(Teacher.id))


class Subject(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    grade = Column(Enum(GRADE))
    number_of_15p = Column(Integer)
    number_of_45p = Column(Integer)


class Student(db.Model):
    id = Column(Integer, ForeignKey(Profile.id), primary_key=True, unique=True)
    grade = Column(Enum(GRADE), default=GRADE.K10)


class Students_Classes(db.Model):
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)


class Teachers_Subject(db.Model):
    id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    teacher_id = Column(Integer, ForeignKey(Teacher.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)


class Teaching_plan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    score_deadline = Column(DateTime)
    teacher_id = Column(Integer, ForeignKey(Teacher.id), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)


class Exam(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    final_points = Column(Float)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    teach_plan_id = Column(Integer, ForeignKey(Teaching_plan.id), nullable=False)
    scores = relationship("Score", backref="exam", lazy=True)


class Score(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    points = Column(Float)
    type = Column(Enum(TYPEEXAM))
    Exam_id = Column(Integer, ForeignKey(Exam.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # p1 = Profile(name="Trần An Tiến")
        # p2 = Profile(name="Nguyễn Sinh Hùng")
        # p3 = Profile(name="Võ Quốc Huy")
        # db.session.add(p3)
        # db.session.commit()
        # acc1 = User(id=p1.id, username="supertien", password="123", user_role=UserRole.ADMIN)
        # acc2 = User(id=p2.id, username="chosh", password="123", user_role=UserRole.STAFF)
        # acc3 = User(id=p3.id, username="mintam", password="123", user_role=UserRole.TEACHER)
        # db.session.add_all([acc1, acc2, acc3])
        # db.session.commit()
        # acc3 = User(id=4, username="qh", password="123", user_role=UserRole.TEACHER)
        # db.session.add(acc3)
        # db.session.commit()
        # staff = Staff(id=acc2.id)
        # teacher = Teacher(id=4, title=Title.BACHELOR)
        # db.session.add( teacher)
        # db.session.commit()

        # =====================================================

        # grade1 = Class(grade = GRADE.K10,count = 1,amount = 40,teacher_id = 3)
        # grade2 = Class(grade = GRADE.K12,count = 1,amount = 40,teacher_id = 3)
        # grade3 = Class(grade = GRADE.K11,count = 1,amount = 40,teacher_id = 3)
        # grade4 = Class(grade = GRADE.K12,count = 1,amount = 40,teacher_id = 3)
        # db.session.add_all([grade1,grade2,grade3,grade4])
        # db.session.commit()

        # semster = Semester(semester_name = "Ki 1")
        # db.session.add(semster)
        # db.session.commit()

        # subjects = [
        #     Subject(name='Toán', grade=GRADE.K10, number_of_15p=2, number_of_45p=1),
        #     Subject(name='Văn', grade=GRADE.K10, number_of_15p=2, number_of_45p=1),
        #     Subject(name='Anh', grade=GRADE.K10, number_of_15p=1, number_of_45p=1),
        #     Subject(name='Lý', grade=GRADE.K11, number_of_15p=2, number_of_45p=1),
        #     Subject(name='Hóa', grade=GRADE.K11, number_of_15p=2, number_of_45p=1),
        #     Subject(name='Sinh', grade=GRADE.K11, number_of_15p=2, number_of_45p=1),
        # ]
        # for subject in subjects:
        #     db.session.add(subject)
        # db.session.commit()
        # teaching_plan = Teaching_plan(
        #     score_deadline=datetime.now(),
        #     teacher_id=4,
        #     class_id=1,
        #     semester_id=1,
        #     subject_id=3
        # )
        # db.session.add(teaching_plan)
        # db.session.commit()

        # profiles_data = [
        #     {"id": 5, "name": "Trần Lưu Quốc Tuấn", "email": "john@example.com", "dob": "2003-01-15", "gender": True,
        #      "address": "123 Main St", "phone": "1234567890"},
        #     {"id": 6, "name": "Nguyễn Thế Anh", "email": "jane@example.com", "dob": "2003-05-20", "gender": False,
        #      "address": "456 Elm St", "phone": "9876543210"},
        #     # Thêm thông tin hồ sơ cho sinh viên khác nếu cần
        # ]
        # for profile_info in profiles_data:
        #     profile = Profile(**profile_info)
        #     db.session.add(profile)
        #
        # # db.session.commit()
        # students_data = [
        #     {"id": 5,  "grade": GRADE.K10},
        #     {"id": 6,  "grade": GRADE.K10},
        #
        #     # Thêm sinh viên khác nếu cần
        # ]
        # #
        # for student_info in students_data:
        #     student = Student(**student_info)
        #     db.session.add(student)
        #
        # db.session.commit()
        # #
        # student_class = Students_Classes(class_id = 1,student_id = 6)
        # db.session.add(student_class)
        # db.session.commit()

