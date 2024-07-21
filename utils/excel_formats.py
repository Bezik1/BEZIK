from dateutil.parser import parse
from openpyxl.styles import numbers

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
    funcs = [(is_int, numbers.FORMAT_NUMBER), (is_date, numbers.FORMAT_DATE_YYYYMMDD2), (is_float, numbers.FORMAT_CURRENCY_USD), (is_str, numbers.FORMAT_TEXT)]

    for func, label in funcs:
        if func(value):
            return label