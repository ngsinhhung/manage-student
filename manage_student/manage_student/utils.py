from datetime import datetime


def get_current_year():
    if datetime.now().month < 6:
        return datetime.now().year - 1
    return datetime.now().year
