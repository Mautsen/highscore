import re

def validate_username(name):
    pattern = r'^[a-zA-Z0-9]{3}$'
    if re.match(pattern, name):
        return True
    else:
        return False