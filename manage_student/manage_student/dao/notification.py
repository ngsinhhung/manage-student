from manage_student.model import *


def create_notify(noi_dung, user_id):
    notification = Notification(noi_dung=noi_dung, user_id=user_id)
    db.session.add(notification)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        create_notify("Thay doi si so lop", 1)
