from flask import render_template, redirect, url_for, request, jsonify
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required, logout_user, login_user
from manage_student import app, login
from manage_student.dao import auth
from manage_student.dao.auth import auth_user, get_info_by_id
from manage_student.dao.student import create_student
from manage_student.dao.teacher import get_class_of_teacher, check_deadline_score, get_teaching_plan_details
from manage_student.form import *
from dao import auth, assignments, teacher
from dao import auth, student, group_class,teacher
from manage_student.model import UserRole
from manage_student import admin

from manage_student.controller.teach import *

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


@app.route('/teacher/assignment', methods=["GET", "POST"])
def teacher_assignment():
    classname = ''
    if request.method.__eq__("POST"):
        classname = request.form.get("class-list")
        grade_value = request.form.get("grade-list")
        return redirect('/teacher/assignment/' + grade_value + '/' + classname)
    return render_template("teacher_assignment.html", classname=classname)

@app.route('/teacher/assignment/<grade>/<string:classname>', methods=["GET", "POST"])
def teacher_assignment_class(grade, classname):
    subject_list = assignments.load_subject_of_class(grade='K' + grade)
    teacher_list = teacher.load_all_teachers()
    if request.method.__eq__("GET"):
        pass
    elif request.method.__eq__("POST"):
        pass
    return render_template("teacher_assignment.html", grade=grade, classname=classname, subjects=subject_list, teachers=teacher_list)





@app.route('/api/class/', methods=['GET'])
def get_class():
    q = request.args.get('q')
    res = {}
    if q:
        class_list = assignments.load_class_by_grade(q)
        json_class_list = [
            {
                "grade": c.grade.value,
                "count": c.count,
            }
            for c in class_list
        ]
        return jsonify({"class_list": json_class_list})
    return jsonify({})


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
@login_required
def InputGrade():
    profile = get_info_by_id(current_user.id)
    return render_template("input_score.html",teacher_class = get_class_of_teacher(profile.id),check_deadline_score = check_deadline_score)

@app.route("/grade/input/<class_id>/score")
@login_required
def InputGradeSubject(class_id):
    class_params = int(class_id.split('=')[-1])
    class_obj,semester,subject,profile_students,teacher_planing = get_teaching_plan_details(class_params)
    return render_template("input_score_subject.html",class_obj=class_obj,semester=semester,subject=subject,profile_students=profile_students,teacher_planing=teacher_planing)

@app.route("/view_score")
def view_grade():
    return render_template("view_score.html")


if __name__ == "__main__":
    with app.app_context():
        from manage_student import admin
        app.run(debug=True)
