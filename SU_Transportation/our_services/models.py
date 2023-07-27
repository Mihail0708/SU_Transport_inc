import os

from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from SU_Transportation.accounts.validators import validate_file_size


class ServicesModel(models.Model):
    service_picture = models.ImageField(upload_to='images', validators=(validate_file_size,))
    service_name = models.CharField(max_length=50)
    service_description = models.TextField()

    def __str__(self):
        return self.service_name


@receiver(pre_delete, sender=ServicesModel)
def delete_related_file(sender, instance, **kwargs):
    if instance.service_picture:
        file_path = instance.service_picture.path
        if os.path.exists(file_path):
            os.remove(file_path)


@receiver(pre_save, sender=ServicesModel)
def replace_related_file(sender, instance,  **kwargs):
    if instance.pk:
        old_instance = ServicesModel.objects.get(pk=instance.pk)
        if old_instance.service_picture:
            old_file_path = old_instance.service_picture.path
            if old_file_path != instance.service_picture.path:
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

