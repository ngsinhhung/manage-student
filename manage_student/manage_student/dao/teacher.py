from manage_student.model import *
from manage_student.utils import *


def get_teacher_not_presidential():
    teachers_is_president = db.session.query(Class.teacher_id).filter(Class.year == get_current_year())
    teachers_not_presidential = db.session.query(Teacher).filter(Teacher.id.not_in(teachers_is_president)).all()
    return teachers_not_presidential


def get_teaching_of_teacher(teacher_id):
    query = db.session.query(Teaching_plan).filter(Teaching_plan.teacher_id == teacher_id).all()
    return query


def get_teaching_plan_by_id(teach_plan_id):
    return Teaching_plan.query.get(teach_plan_id)


def get_score_by_student_id(teach_plan_id,student_id, type,count):
    return db.session.query(Score).join(Exam).filter(Exam.teach_plan_id == teach_plan_id)\
                                                .filter(Exam.student_id == student_id)\
                                                .filter(Score.type == type)\
                                                .filter(Score.count == count).first()


def can_edit_exam(student_id, teach_plan_id):
    e = db.session.query(Exam).filter(Exam.student_id == student_id).filter(teach_plan_id == teach_plan_id).first()
    if e:
        return True
    return False


if __name__ == '__main__':
    with app.app_context():
        print(get_score_by_student_id(1,7,"EXAM_15p",3))
