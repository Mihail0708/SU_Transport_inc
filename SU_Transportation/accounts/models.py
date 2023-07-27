import os

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.dispatch import receiver

from SU_Transportation.accounts.validators import only_letters, validate_file_size
from django.db.models.signals import pre_save, pre_delete


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


@receiver(pre_delete, sender=SuUser)
def delete_related_file(sender, instance, **kwargs):
    if instance.profile_picture:
        file_path = instance.profile_picture.path
        if os.path.exists(file_path):
            os.remove(file_path)


@receiver(pre_save, sender=SuUser)
def replace_related_file(sender, instance,  **kwargs):
    if instance.pk:
        old_instance = SuUser.objects.get(pk=instance.pk)
        if old_instance.profile_picture:
            old_file_path = old_instance.profile_picture.path
            if os.path.exists(old_file_path):
                os.remove(old_file_path)