from flask import redirect
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from manage_student.model import *
from manage_student import app
from flask_login import logout_user, current_user


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


class RegulationsView(AuthenticatedView):
    column_labels = {
        'type': 'Loại quy định',
        'regulation_name': 'Tên quy định',
        'min': 'Giá trị tối thiểu',
        'max': 'Giá trị tối đa',
    }

admin = Admin(app, name='Quản lý học sinh', template_mode='bootstrap4')
admin.add_view(AuthenticatedView(Subject, db.session, name="Danh sách môn học"))
admin.add_view(RegulationsView(Regulation, db.session, name="Chỉnh sửa quy định"))
admin.add_view(LogoutView(name='Đăng xuất'))