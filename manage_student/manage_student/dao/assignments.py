from manage_student import db
from manage_student.model import *

def load_class_by_grade(grade):
    return Class.query.filter_by(grade=grade)

def load_subject_of_class(grade):
    return Subject.query.filter_by(grade=grade)

def load_assignments_of_class(classname):
    pass

if __name__ == '__main__':
    with app.app_context():
        pass