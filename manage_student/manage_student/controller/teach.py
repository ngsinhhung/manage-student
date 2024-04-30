from flask import request, jsonify

from manage_student.model import *

from flask import request, jsonify


@app.route('/api/exam/<int:teaching_plan_id>/scores', methods=['POST'])
def enter_scores(teaching_plan_id):
    try:
        data = request.json
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON data")

        for student_id, scores in data.items():
            # Retrieve or create exam
            exam = Exam.query.filter_by(student_id=student_id, teach_plan_id=teaching_plan_id).first()
            if exam is None:
                exam = Exam(student_id=student_id, teach_plan_id=teaching_plan_id)
                db.session.add(exam)

            # Add 15-minute exam scores
            for score_15p_value in scores.get("15p", []):
                score_15p = Score(points=score_15p_value, type=TYPEEXAM.EXAM_15P)
                exam.scores.append(score_15p)

            # Add 45-minute exam scores
            for score_45p_value in scores.get("45p", []):
                score_45p = Score(points=score_45p_value, type=TYPEEXAM.EXAM_45P)
                exam.scores.append(score_45p)

            # Set final points
            exam.final_points = scores.get("thi", 0)

        db.session.commit()

        return jsonify({"message": "Scores entered successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/exam/<int:subject_id>', methods=['PUT'])
def edit_exam(subject_id):
    pass
