from manage_student.model import *
from manage_student.utils import *


def get_teacher_not_presidential():
    teachers_is_president = db.session.query(Class.teacher_id).filter(Class.year == get_current_year())
    teachers_not_presidential = db.session.query(Teacher).filter(Teacher.id.not_in(teachers_is_president)).all()
    return teachers_not_presidential

def load_all_teachers():
    return Teacher.query.all()
    # return db.session.query(Profile).join(Teacher, Profile.id == Teacher.id).all()
def get_class_of_teacher(teacher_id):
    query = db.session.query(Subject, Class.id, Class.grade, Class.count, Teacher). \
        join(Teaching_plan, Teaching_plan.subject_id == Subject.id). \
        join(Class, Class.id == Teaching_plan.class_id). \
        join(Teacher, Teacher.id == Teaching_plan.teacher_id).filter(Teaching_plan.teacher_id == teacher_id).all()
    return query


def check_deadline_score(subject_id):
    teaching_plan = Teaching_plan.query.filter_by(subject_id=subject_id).first()
    if not teaching_plan:
        return False
    score_deadline = teaching_plan.score_deadline
    current_time = datetime.now()
    if current_time <= score_deadline:
        return True


def get_teaching_plan_details(class_id):
    teaching_plan = Teaching_plan.query.filter_by(class_id=class_id).first()
    class_obj = Class.query.get(class_id)
    semester = Semester.query.get(teaching_plan.semester_id)
    subject = Subject.query.get(teaching_plan.subject_id)
    subquery = db.session.query(Students_Classes.student_id).filter_by(class_id=class_id).subquery()
    profile_students = db.session.query(Profile).filter(Profile.id.in_(subquery)).all()

    return class_obj, semester, subject, profile_students, teaching_plan


def get_exam_for_edition_query(student_id, teaching_plan_id, exam_type):
    return db.session.query(Score.id, Score.type).join(Exam).filter(
        Exam.student_id == student_id,
        Exam.teach_plan_id == teaching_plan_id,
        Score.type == exam_type
    ).all()
