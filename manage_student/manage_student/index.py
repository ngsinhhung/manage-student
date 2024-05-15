from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required, logout_user, login_user
from flask_mail import Message

from manage_student import app, login, mail
from manage_student.dao import regulation, notification
from manage_student.decorators import role_only

from dao import auth, group_class, teacher, assignments
from manage_student import login
from manage_student.api.student_class import *
from manage_student.api.student_score import *
from manage_student.dao.student import *
from manage_student.form import *
from dao import auth, student, group_class, teacher, assignments
from manage_student.api import *
from manage_student.model import UserRole
import datetime
from manage_student.api.teach import *
from manage_student.admin import *


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
    return render_template('login.html', form=form, mse=mse)


@app.route("/log_out")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/home')
@login_required
@role_only([UserRole.STAFF, UserRole.TEACHER])
def home():
    profile = auth.get_info_by_id(current_user.id)
    notifications = notification.load_all_notifications()
    return render_template("index.html", profile=profile, notifications=notifications)


@app.route('/teacher/assignment', methods=["GET", "POST"])
@login_required
@role_only([UserRole.STAFF])
def teacher_assignment():
    classname = ''
    if request.method.__eq__("POST"):
        classname = request.form.get("class-list")
        grade_value = request.form.get("grade-list")
        return redirect('/teacher/assignment/' + grade_value + '/' + classname)
    return render_template("teacher_assignment.html", classname=classname)


@app.route('/teacher/assignment/<grade>/<string:classname>', methods=["GET", "POST", "DELETE"])
@login_required
@role_only([UserRole.STAFF])
def teacher_assignment_class(grade, classname):
    subject_list = assignments.load_subject_of_class(grade='K' + grade)
    class_id = group_class.get_info_class_by_name(grade=grade, count=classname[3:]).id
    if request.method.__eq__("GET"):
        plan = assignments.load_assignments_of_class(class_id=class_id)
        return render_template("teacher_assignment.html", grade=grade, classname=classname, subjects=subject_list,
                               get_teachers=assignments.load_all_teacher_subject, plan=plan)
    elif request.method.__eq__("POST") and request.form.get("type").__eq__("save"):
        for s in subject_list:
            teacher_id = request.form.get("teacher-assigned-{id}".format(id=s.id))
            total_seme = request.form.get("total-seme-{id}".format(id=s.id))
            seme1 = request.form.get("seme1-{id}".format(id=s.id))
            seme2 = request.form.get("seme2-{id}".format(id=s.id))
            semester_id = None
            if total_seme:
                semester_id = [1, 2]
            elif seme1:
                semester_id = 1
            elif seme2:
                semester_id = 2
            assignments.save_subject_assignment(
                teacher_id=teacher_id,
                class_id=class_id,
                semester_id=semester_id,
                subject_id=s.id
            )
        return redirect("/teacher/assignment/{grade}/{classname}".format(grade=str(grade), classname=classname))
    elif request.method.__eq__("POST") and request.form.get("type").__eq__("delete"):
        assignments.delete_assignments(class_id)
        return render_template("teacher_assignment.html", grade=grade, classname=classname, subjects=subject_list,
                               get_teachers=assignments.load_all_teacher_subject)
    return render_template("teacher_assignment.html", grade=grade, classname=classname, subjects=subject_list,
                           get_teachers=assignments.load_all_teacher_subject)

@app.route('/api/class/', methods=['GET'])
@role_only([UserRole.STAFF])
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

def send_mail(subject, recipients, student_name, classname):
    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'],
                  recipients=recipients)
    msg.html = render_template("/email/email.html", student_name=student_name, classname=classname)
    mail.send(msg)
    return "Message sent!"

@app.route('/class/create', methods=['GET', 'POST'])
def create_class():
    form_create_class = CreateClass()
    form_create_class.teacher.choices = [(temp_teacher.id, temp_teacher.user.profile.name) for temp_teacher in
                                         teacher.get_teacher_not_presidential()]
    if request.method == "POST" and form_create_class.validate_on_submit():
        try:
            temp_class = group_class.create_class(form_create_class)
        except Exception as e:
            redirect("/home")
        redirect(url_for("index"))
    return render_template("create_class.html", form_create_class=form_create_class, list_class=group_class.get_class(),
                           student_no_class=student.student_no_class())


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
            return render_template("register_student.html", form_student=form_student)
        if s:
            return redirect(url_for("index"))
    return render_template("register_student.html", form_student=form_student)


@app.route('/<int:grade>/<int:count>/info')
def info(grade, count):
    class_info = group_class.get_info_class_by_name(grade, count)
    student_no_class = student.student_no_class("K" + str(grade))
    return render_template("class_info.html", class_info=class_info, student_no_class=student_no_class)


@app.route("/regulations")
def view_regulations():
    regulations = regulation.get_regulations()
    return render_template('view_regulations.html', regulations=regulations)


@app.route("/grade")
@login_required
def input_grade():
    profile = auth.get_info_by_id(current_user.id)
    return render_template("input_score.html", teaching_plan=teacher.get_teaching_of_teacher(profile.id),date=datetime.now())


@app.route("/grade/input/<teach_plan_id>/score")
@login_required
def input_grade_subject(teach_plan_id):
    teach_plan = teacher.get_teaching_plan_by_id(teach_plan_id)
    return render_template("input_score_subject.html", can_edit=teacher.can_edit_exam, get_score=teacher.get_score_by_student_id,teach_plan=teach_plan)

@app.route("/cc")
def test():
    return render_template("test.html")

@app.route("/view_score", methods=['GET', 'POST'])
def view_score():
    semester = get_all_semester()
    return render_template("view_score.html", semester=semester)
if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
