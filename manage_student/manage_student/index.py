from flask import render_template, redirect, url_for
from flask_login import current_user, login_required, logout_user, login_user

from dao import auth, group_class, teacher, assignments
from manage_student import login
from manage_student.api.student_class import *
from manage_student.api.student_score import *
from manage_student.dao.student import *
from manage_student.form import *
from manage_student.model import UserRole
import datetime
from manage_student.api.teach import *
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
        user = auth.auth_user(username=username, password=password)
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
    profile = auth.get_info_by_id(current_user.id)
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
    if request.method.__eq__("POST"):
        grade = grade
        class_count = classname[-1]
        print(request.form)
        for s in subject_list:
            print(request.form.get("teacher-assigned-{id}".format(id=s.id)))

    elif request.method.__eq__("GET"):
        print("get")
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
            s = student.create_student(form_student)
        except Exception as e:
            print(e)
            return render_template("register_student.html",form_student=form_student)
        if s:
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
def input_grade():
    profile = auth.get_info_by_id(current_user.id)
    return render_template("input_score.html", teaching_plan=teacher.get_teaching_of_teacher(profile.id),date=datetime.datetime.now())


@app.route("/grade/input/<teach_plan_id>/score")
@login_required
def input_grade_subject(teach_plan_id):
    teach_plan = teacher.get_teaching_plan_by_id(teach_plan_id)
    return render_template("input_score_subject.html", can_edit=teacher.can_edit_exam, get_score=teacher.get_score_by_student_id,teach_plan=teach_plan)


@app.route("/view_score", methods=['GET', 'POST'])
def view_score():
    semester = get_all_semester()
    return render_template("view_score.html", semester=semester)
if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
