from flask import render_template

from manage_student import app
from manage_student.form import *

app.config['SECRET_KEY'] = 'secretkey'
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.SubmitFieldLogin():
        username = form.username.data
        password = form.password.data
        print(username)
        print(password)
    return render_template('login.html', form=form)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/teacher/assignment')
def teacher_assignment():
    return render_template("teacher_assignment.html")


@app.route('/class/create', methods=['GET', 'POST'])
def create_class():
    form_create_class = CreateClass()
    if form_create_class.validate_on_submit():
        pass
    return render_template("create_class.html",form_create_class=form_create_class)


@app.route('/class/edit')
def class_edit():
    return render_template("list_class.html")


@app.route('/student/register')
def register():
    form_student = AdmisionStudent()
    if form_student.validate_on_submit():
        pass
    return render_template("register_student.html", form_student=form_student)


@app.route('/<class_id>/info')
def info(class_id):
    return render_template("class_info.html", class_id=class_id)


@app.route("/regulations")
def view_regulations():
    return render_template('view_regulations.html')

@app.route("/grade")
def InputGrade():
    return render_template("input_score.html")
@app.route("/grade/input")
def InputGradeSubject():
    return render_template("input_score_subject.html")

@app.route("/grade")
def view_grade():
    return render_template("view_score.html")


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
