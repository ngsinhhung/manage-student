
from flask import jsonify,request
from manage_student import app
from manage_student.dao.student import view_score_student, preprocess_scores


@app.route("/api/view_score/<int:student_id>", methods=['GET'])
def view_semester(student_id):
    semester_id = request.args.get('semester_id')
    score = view_score_student(student_id, semester_id)
    processed_scores = preprocess_scores(score)
    return jsonify(processed_scores)


