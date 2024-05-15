from manage_student.model import *

def get_regulations():
    return Regulation.query.all()

