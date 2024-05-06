from flask import render_template, redirect, url_for,request
from flask_login import current_user, login_required, logout_user, login_user
from manage_student import app, login
from manage_student.dao.auth import auth_user, get_info_by_id
from manage_student.dao.student import create_student
from manage_student.form import *
from dao import auth, student, group_class,teacher
from manage_student.model import UserRole
from manage_student import admin


@login.user_loader
def user_load(user_id):
    return auth.load_user(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.ADMIN:
            return redirect("/admin")
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    mse = ""
    form = LoginForm()
    if request.method == "POST" and form.SubmitFieldLogin():
        username = form.username.data
        password = form.password.data
        user = auth_user(username=username, password=password)
        if user:
            login_user(user)
            return redirect(url_for("index"))
        mse = "Tài khoản hoặc mật khẩu không đúng"
    return render_template('login.html', form=form,mse=mse)


@app.route("/log_out")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/home')
@login_required
def home():
    profile = get_info_by_id(current_user.id)
    return render_template("index.html", profile=profile)


@app.route('/teacher/assignment')
def teacher_assignment():
    return render_template("teacher_assignment.html")


@app.route('/class/create', methods=['GET', 'POST'])
def create_class():
    form_create_class = CreateClass()
    form_create_class.teacher.choices = [(temp_teacher.id,temp_teacher.user.profile.name)for temp_teacher in teacher.get_teacher_not_presidential()]
    if request.method == "POST" and form_create_class.validate_on_submit():
        try:
            temp_class = group_class.create_class(form_create_class)
        except Exception as e:
            redirect("/home")
        redirect(url_for("index"))
    return render_template("create_class.html", form_create_class=form_create_class, list_class=group_class.get_class(),student_no_class=student.student_no_class())


@app.route('/class/edit')
def class_edit():
    classes = group_class.get_class()
    return render_template("list_class.html", classes=classes)


@app.route('/student/register', methods=['GET', 'POST'])
def register():
    form_student = AdmisionStudent()

    if request.method == "POST" and form_student.submit():
        try:
            student = create_student(form_student)
        except Exception as e:
            print(e)
            return render_template("register_student.html",form_student=form_student)
        if student:
            return redirect(url_for("index"))
    return render_template("register_student.html",form_student=form_student)


@app.route('/<int:grade>/<int:count>/info')
def info(grade,count):
    class_info = group_class.get_info_class_by_name(grade,count)
    student_no_class = student.student_no_class("K"+str(grade))
    return render_template("class_info.html",class_info=class_info,student_no_class=student_no_class)


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
