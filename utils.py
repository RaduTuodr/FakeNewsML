import re


WINDOW_HEIGHT = 625
WINDOW_WIDTH = 415


def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False
