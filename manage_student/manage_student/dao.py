from .model import *

def get_class_of_teacher(teacher_id):
    query = db.session.query(Subject, Class.grade,Class.count, Teacher). \
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
def get_teaching_plan_details(subject_id):

    teaching_plan = Teaching_plan.query.filter_by(subject_id=subject_id).first()
    class_obj = Class.query.get(teaching_plan.class_id)
    semester = Semester.query.get(teaching_plan.semester_id)
    subject = Subject.query.get(subject_id)

    subquery = db.session.query(Students_Classes.student_id).filter_by(class_id=class_obj.id).subquery()

    profile_students = db.session.query(Profile).filter(Profile.id.in_(subquery)).all()
    return class_obj, semester, subject, profile_students

