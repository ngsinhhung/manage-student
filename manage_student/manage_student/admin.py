from flask import redirect, request
from flask_admin import Admin, expose, AdminIndexView
from flask_admin import BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from manage_student.dao import subject,semester,group_class

from manage_student import app
from manage_student.model import *


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')

    def is_accessible(self):
        return current_user.is_authenticated


class StatView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html',list_subject=subject.get_all_subjects(),list_semester=semester.get_all_semester())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


# class MyAdminIndexView(AdminIndexView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/index.html')
class StatInfoView(BaseView):
    @expose('/')
    def index(self):

        res = subject.get_avg_score_by_class(request.args.get("semester"),request.args.get("subject"))
        list_class_id = [t[0] for t in res]
        list_dtb = [t[1] for t in res]
        return self.render('admin/stats_info.html',subject_info=subject.get_subject_by_id(request.args.get("subject")),list_class_id=list_class_id,list_dtb=list_dtb,def_get_class=group_class.get_class_by_id)

    def is_visible(self):
        return False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin = Admin(app, name='Quản lý học sinh', template_mode='bootstrap4')
admin.add_view(AuthenticatedView(Subject, db.session))
admin.add_view(StatView(name='Thống kê'))
admin.add_view(StatInfoView(name="Thống kê chi tiết"))
admin.add_view(LogoutView(name='Đăng xuất'))
