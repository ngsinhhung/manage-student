from manage_student.model import User


def load_user(user_id):
    return User.query.get(user_id)