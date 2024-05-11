from sqlalchemy import func, case

from manage_student import db,app
from manage_student.model import Subject,Class,Exam,Teaching_plan,Score,Student, Students_Classes


def get_all_subjects():
    return Subject.query.all()


def get_subject_by_id(id):
    return Subject.query.get(id)


def get_avg_score_by_class(semester_id,s_id):
    student_dtb = db.session.query(Student.id.label("id"), (func.sum(case((Score.type == "EXAM_15P", Score.score * 1),(Score.type == "EXAM_45P", Score.score * 2),(Score.type == "EXAM_final", Score.score * 3))) /
                                                                       func.sum(case((Score.type == "EXAM_15P", 1),(Score.type == "EXAM_45P", 2),(Score.type == "EXAM_final", 3)))).label('diem_trung_binh')). \
                            join(Exam,Student.id == Exam.student_id).join(Score).join(Teaching_plan).filter(Teaching_plan.subject_id == s_id).filter(Teaching_plan.semester_id ==semester_id).group_by(Student.id).subquery()

    query_result = db.session.query(Students_Classes.class_id, func.avg(student_dtb.c.diem_trung_binh)). \
                                    join(student_dtb, student_dtb.c.id == Students_Classes.student_id). \
             group_by(Students_Classes.class_id).all()
    return query_result


if __name__ == '__main__':
    with app.app_context():
        print([t[0] for t in get_avg_score_by_class(2,1)])

