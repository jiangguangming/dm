from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def verify_data(data, essential_keys=[], optional_keys=[]):
    data_list = set(data.keys())
    if not (data_list >= set(essential_keys)):
        return False
    full_keys = set(essential_keys).union(set(optional_keys))
    if not (full_keys >= data_list):
        return False
    return True

def verify_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError as e:
        return False