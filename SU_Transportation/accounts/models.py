from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from SU_Transportation.accounts.validators import only_letters, validate_file_size


class SuUser(AbstractUser):
    CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(validators=(MinLengthValidator(2), MaxLengthValidator(15), only_letters))
    last_name = models.CharField(validators=(MinLengthValidator(2), MaxLengthValidator(15), only_letters))
    profile_picture = models.ImageField(upload_to='images', validators=(validate_file_size,), blank=True, null=True)
    gender = models.CharField(max_length=7, choices=CHOICES)
    is_driver = models.BooleanField(default=False)

