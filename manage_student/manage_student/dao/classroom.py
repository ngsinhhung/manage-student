from manage_student.model import *

def load_class(grade):
    return Class.query.filter(Class.grade == grade)

def add_new_classmate():
    pass