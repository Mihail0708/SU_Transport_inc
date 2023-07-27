from django.core.exceptions import ValidationError


def positive_number(value):
    str_value = str(value)
    if str_value[0] == '-':
        raise ValidationError("Positive number only!")
