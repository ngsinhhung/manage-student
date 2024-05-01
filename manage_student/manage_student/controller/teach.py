
from manage_student.model import *
from flask import request, jsonify


@app.route('/api/exam/<int:teaching_plan_id>/scores', methods=['POST'])
def enter_scores(teaching_plan_id):
    try:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON data")

        teaching_plan = Teaching_plan.query.get_or_404(teaching_plan_id)
        subject = Subject.query.get_or_404(teaching_plan.subject_id)
        number_of_15p = subject.number_of_15p
        number_of_45p = subject.number_of_45p

        for student_id, scores in data.items():
            exam = Exam.query.filter_by(student_id=student_id, teach_plan_id=teaching_plan_id).first()
            if exam is None:
                exam = Exam(student_id=student_id, teach_plan_id=teaching_plan_id)
                db.session.add(exam)

            if len(scores.get("score_15p", [])) != number_of_15p or len(scores.get("score_45p", [])) != number_of_45p:
                raise ValueError("Invalid number of scores")

            for score_15p_value in scores.get("score_15p", []):
                score_15p = Score(points=score_15p_value, type=TYPEEXAM.EXAM_15P)
                exam.scores.append(score_15p)

            for score_45p_value in scores.get("score_45p", []):
                score_45p = Score(points=score_45p_value, type=TYPEEXAM.EXAM_45P)
                exam.scores.append(score_45p)

            exam.final_points = scores.get("score_final", 0)

        db.session.commit()

        return get_score_students()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@app.route('/api/exam/get_score_student/scores', methods=['GET'])
def get_score_students():
    try:
        scores_data = {}
        exams = Exam.query.all()
        for exam in exams:
            scores_data[exam.student_id] = {
                "score_15p": [score.points for score in exam.scores if score.type == TYPEEXAM.EXAM_15P],
                "score_45p": [score.points for score in exam.scores if score.type == TYPEEXAM.EXAM_45P],
                "score_final": exam.final_points
            }

        return jsonify(scores_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/exam/<int:subject_id>', methods=['PUT'])
def edit_exam(subject_id):
    pass
