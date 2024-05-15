from datetime import datetime

from manage_student import app


def get_current_year():
    if datetime.now().month < 6:
        return datetime.now().year - 1
    return datetime.now().year

if __name__ == '__main__':
    with app.app_context():
        print(get_current_year())
