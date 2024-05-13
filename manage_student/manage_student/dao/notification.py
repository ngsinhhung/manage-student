from manage_student.model import Notification


def load_all_notifications():
    return Notification.query.all()
