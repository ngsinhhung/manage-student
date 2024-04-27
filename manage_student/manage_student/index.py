
from flask import render_template

from manage_student import app
from manage_student.dao import *
from manage_student.form import *
from manage_student.controller import *
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.SubmitFieldLogin():
        username = form.username.data
        password  = form.password.data
        print(username)
        print(password)
    return render_template('login.html', form=form)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/teacher/assignment')
def teacher_assignment():
    return render_template("teacher_assignment.html")


@app.route('/class/create',methods=['GET', 'POST'])
def create_class():
    form_create_class = CreateClass()
    if form_create_class.validate_on_submit():
        pass
    return render_template("create_class.html",form_create_class=form_create_class)


@app.route('/class/edit')
def class_edit():
    return render_template("list_class.html")


@app.route('/student/create')
def register():
    form_student = AdmisionStudent()
    if form_student.validate_on_submit():
        pass
    return render_template("register_student.html",form_student=form_student)


@app.route('/<class_id>/info')
def info(class_id):
    return render_template("class_info.html", class_id=class_id)


@app.route("/regulations")
def view_regulations():
    return render_template('view_regulations.html')

@app.route("/grade")
def InputGrade():
    return render_template("input_score.html",teacher_class = get_class_of_teacher(3),check_deadline_score = check_deadline_score)

@app.route("/grade/input/<subject_id>")
def InputGradeSubject(subject_id):
    subject_params = int(subject_id.split('=')[-1])
    class_obj,semester,subject,profile_students = get_teaching_plan_details(subject_params)
    print(profile_students)
    return render_template("input_score_subject.html",class_obj=class_obj,semester=semester,subject=subject,profile_students=profile_students)

@app.route("/view_score")
def view_grade():
    return render_template("view_score.html")



if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
