import re

def is_valid_russian_phone_number(phone:str):
    pattern = r'^(?:\+7|8)?\d{10}$'
    return bool(re.match(pattern, phone))