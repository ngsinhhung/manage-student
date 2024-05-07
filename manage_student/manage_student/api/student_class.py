from flask import request, jsonify

from manage_student import app,db
from manage_student.model import Student, Students_Classes
from manage_student.dao import student,group_class


@app.route('/api/add_student/<int:class_id>', methods=['post'])
def add_student(class_id):
    list_student = request.json['list_student']
    for s in list_student:
        student_class = Students_Classes(student_id=s, class_id=class_id)
        db.session.add(student_class)
        db.session.commit()
    return jsonify({'status': 200})


@app.route('/api/delete_student/<int:class_id>', methods=['delete'])
def delete_student(class_id):
    list_student = request.json['list_student']
    for s in list_student:
        tmp = student.check_student_in_class(student_id=s, class_id=class_id)
        db.session.delete(tmp)
        db.session.commit()
    return jsonify({'status': 404})
