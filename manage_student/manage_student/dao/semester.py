from manage_student.model import Semester


def get_all_semester():
    return Semester.query.order_by(Semester.id.desc()).all()