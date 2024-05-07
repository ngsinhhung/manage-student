from flask import request, jsonify

from manage_student.dao.teacher import get_exam_for_edition_query
from manage_student.model import *


def extract_scores(exam):
    return {
        "score_15p": [score.points for score in exam.scores if score.type == TYPEEXAM.EXAM_15P],
        "score_45p": [score.points for score in exam.scores if score.type == TYPEEXAM.EXAM_45P],
        "score_final": exam.final_points
    }


def update_scores(scores, values):
    for score, value in zip(scores, values):
        if value is not None:
            db.session.query(Score).filter(
                Score.id == score.id
            ).update({"points": value})


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
            scores_data[exam.student_id] = extract_scores(exam)
        return jsonify(scores_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/exam/get_score_student/<int:student_id>/scores', methods=['GET'])
def get_student_scores(student_id):
    try:
        exam = Exam.query.filter_by(student_id=student_id).first()
        if exam:
            scores_data = extract_scores(exam)
            return jsonify(scores_data), 200
        else:
            return jsonify({"message": "Exam does not exist"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/exam/<int:student_id>/edit_score', methods=['PUT'])
def edit_exam(student_id):
    try:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON data")

        teaching_plan = Teaching_plan.query.join(Exam, Teaching_plan.id == Exam.teach_plan_id) \
            .filter(Exam.student_id == student_id).first()

        if teaching_plan is None:
            return jsonify({"message": "Not found teaching plan for the student"}), 500

        exam_15p_query = get_exam_for_edition_query(student_id, teaching_plan.id, TYPEEXAM.EXAM_15P)
        exam_45p_query = get_exam_for_edition_query(student_id, teaching_plan.id, TYPEEXAM.EXAM_45P)

        score_15p_values = data.get("score_15p", [])
        score_45p_values = data.get("score_45p", [])

        update_scores(exam_15p_query, score_15p_values)
        update_scores(exam_45p_query, score_45p_values)

        db.session.query(Exam).filter(
            Exam.student_id == student_id,
            Exam.teach_plan_id == teaching_plan.id
        ).update(
            {"final_points": data.get("score_final")}
        )

        db.session.commit()
        return jsonify({'message': 'Exam successfully updated'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
