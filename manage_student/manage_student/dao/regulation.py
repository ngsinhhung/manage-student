from manage_student.model import *


def get_regulations():
    return Regulation.query.all()


def get_regulation_by_name(name):
    return db.session.query(Regulation).filter(Regulation.regulation_name == name).first()

