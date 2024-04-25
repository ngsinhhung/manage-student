from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, SelectField,DateField,IntegerField
from wtforms.validators import InputRequired, Length, Email, NumberRange, Regexp, DataRequired, ValidationError
import re

def validate_phone_number(form,field):
    phone_number =  field.data
    if not re.match(r'^\d+$', phone_number):
        raise ValidationError('Số điện thoại chỉ được chứa các chữ số.')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Tên đăng nhập"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Mật khẩu"})
    SubmitFieldLogin = SubmitField("Đăng nhập")

class AdmisionStudent(FlaskForm):
    full_name = StringField("Họ và tên", validators=[InputRequired("Vui Lòng nhập họ tên học sinh"), Length(max=100)],
                            render_kw={"placeholder": "Nhập họ và tên"})
    gender = SelectField("Giới tính", choices=[("0", "Nam"), ("1", "Nữ")],
                         validators=[InputRequired()],
                         render_kw={"placeholder": "Chọn giới tính"})
    birth_date = DateField("Ngày sinh", validators=[InputRequired()],
                           render_kw={"placeholder": "Chọn ngày sinh"},format="%d-%m-%y")
    address = StringField("Địa chỉ", validators=[InputRequired(), Length(max=255)],
                          render_kw={"placeholder": "Nhập địa chỉ"})
    phone_number = StringField("Số điện thoại", validators=[
        InputRequired(message="Vui lòng nhập số điện thoại"),
        Length(min=10, max=11, message="Số điện thoại phải từ 10 đến 11 chữ số"),
        validate_phone_number
    ], render_kw={"placeholder": "Nhập số điện thoại"})
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=100)],
                        render_kw={"placeholder": "Nhập email"})
    submit = SubmitField("Gửi")


class CreateClass(FlaskForm):
    teacher = StringField("Giáo viên chủ nhiệm", validators=[InputRequired()],
                          render_kw={"placeholder": "Nhập tên giáo viên chủ nhiệm"})
    grade = SelectField("Khối học", choices=[("K10", "Khối 10"), ("K11", "Khối 11"), ("K12", "Khối 12")],
                        validators=[InputRequired()],
                        render_kw={"placeholder": "Chọn khối học"})
    class_size = IntegerField("Số lượng học sinh", validators=[InputRequired(), NumberRange(min=0)],
                              render_kw={"placeholder": "Sỉ số lớp"})
    submit = SubmitField("Lưu")



