import re

def is_valid_russian_phone_number(phone: str):#TODO django-phone-number lib instead this
    pattern = r"^(?:\+7|8)\d{10}$"
    return bool(re.match(pattern, phone))
