from dateutil.parser import parse

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_date(date_str):
    try:
        parse(date_str, fuzzy=False)
        return True
    except ValueError:
        return False

def is_str(value):
    try:
        str(value)
        return True
    except ValueError:
        return False

def map_format(value):
    funcs = [(is_int, '0'), (is_date, 'yyyy-mm-dd'), (is_float, '0.00'), (is_str, '@')]

    for func, label in funcs:
        if func(value):
            return label