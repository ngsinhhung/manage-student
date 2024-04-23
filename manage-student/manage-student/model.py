# from datetime import datetime
#
# from flask_login import UserMixin
# from sqlalchemy import Column, String, Float, Integer, ForeignKey, Boolean, DateTime, Enum, Text
# from sqlalchemy.orm import relationship
# from manage-student import db, app
# import enum
#
#
# class UserRole(enum.Enum):
#     STAFF = 1
#     TEACHER = 2
#     ADMIN = 3
#
#
# class Title(enum.Enum):
#     BACHELOR = 1
#     MASTER = 2
#     DOCTOR = 3
#
#
# class GRADE(enum.Enum):
#     K10 = 1
#     K11 = 2
#     K12 = 3
#
#
# class TYPEEXAM(enum.Enum):
#     EXAM_15P = 1
#     EXAM_45P = 2
#
#
# class Semester(db.Model):
#     id = Column(Integer, primary_key=True,autoincrement=True)
#     semester_name = Column(String(50))
#
#
# class Profile(db.Model):
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     name = Column(String(50))
#     email = Column(String(50), unique=True)
#     dob = Column(DateTime)
#     gender = Column(Boolean)
#     address = Column(Text)
#     phone = Column(String(10), unique=True)
#
#
# class User(db.Model, UserMixin):
#     id = Column(Integer, ForeignKey(Profile.id), primary_key=True, nullable=False, unique=True)
#     username = Column(String(50), unique=True)
#     password = Column(String(50))
#     user_role = Column(Enum(UserRole))
#     notifications = relationship("Notification", backref="user", lazy=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Staff(db.Model):
#     id = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True, nullable=False)
#
#
# class Teacher(db.Model):
#     id = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True, nullable=False)
#     title = Column(Enum(Title))
#
#     class_teach = relationship("Class", backref="class_teach", lazy=True)
#
#
# class Notification(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     noi_dung = Column(Text)
#     created_at = Column(DateTime, default=datetime.now())
#     user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
#
#
# class Class(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     grade = Column(Enum(GRADE))
#     count = Column(Integer)
#     amount = Column(Integer, default=0)
#     teacher_id = Column(Integer, ForeignKey(Teacher.id))
#
#
# class Subject(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50))
#     grade = Column(Enum(GRADE))
#     number_of_15p = Column(Integer)
#     number_of_45p = Column(Integer)
#
#
# class Student(db.Model):
#     id = Column(Integer, ForeignKey(Profile.id), primary_key=True, unique=True)
#     grade = Column(Enum(GRADE), default=GRADE.K10)
#
#
# class Students_Classes(db.Model):
#     id = Column(Integer, primary_key=True, nullable=False)
#     class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
#     student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
#
#
# class Teaching_plan(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     score_deadline = Column(DateTime)
#     teacher_id = Column(Integer, ForeignKey(Teacher.id), nullable=False)
#     class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
#     semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
#
#
# class Exam(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     final_points = Column(Float)
#     student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
#     teach_plan_id = Column(Integer, ForeignKey(Teaching_plan.id), nullable=False)
#     scores = relationship("Score", backref="exam", lazy=True)
#
#
# class Score(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     points = Column(Float)
#     type = Column(Enum(TYPEEXAM))
#     Exam_id = Column(Integer, ForeignKey(Exam.id), nullable=False)
#
#
# # if __name__ == '__main__':
# #     with app.app_context():
# #         db.create_all()
#         # p = Profile(name="tat")
#         # db.session.add(p)
#         # db.session.commit()
#         # acc = User(id=p.id,username="cccc",password="123")
#         # db.session.add(acc)
#         # db.session.commit()
#         # # src.run(debug=True)
