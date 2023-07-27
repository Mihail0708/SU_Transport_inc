from django.core.exceptions import ValidationError


def validate_file_size(image_obj):
    size = 700 * 1024
    if image_obj.size > size:
        raise ValidationError("The maximum file size should be 700 KB")


def only_letters(name):
    for char in name:
        if not char.isalpha():
            raise ValidationError('Name must contain letters only')


def only_integers(value):
    value_str = str(value)
    for char in value_str:
        if not char.isdigit():
            raise ValidationError('The field should content only integers')