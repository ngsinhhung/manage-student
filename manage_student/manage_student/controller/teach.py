
from flask import render_template, jsonify,request

from manage_student import app,db
from manage_student.model import Exam, Score


@app.route("/api/subject_score/<subject_id>", methods=['POST'])
def input_grades(subject_id):
    print(subject_id)
    data = request.json
    if data is None:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    try:
        for exam_id, scores in data.items():
            for exam_type, score_value in scores.items():
                student_id = scores['student_id']
                exam = Exam.query.filter_by(id=exam_id, student_id=student_id).first()
                if exam is None:
                    return jsonify({"error": f"Không tìm thấy kỳ thi với ID {exam_id} cho học sinh {student_id}"}), 404
                score = Score(points=score_value, type=exam_type, Exam_id=exam.id)
                db.session.add(score)

        db.session.commit()
        return jsonify({"message": "Đã cập nhật điểm thành công"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Lỗi khi cập nhật điểm: {str(e)}"}), 500
