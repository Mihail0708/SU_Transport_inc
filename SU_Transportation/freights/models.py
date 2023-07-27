import os

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from SU_Transportation.accounts.validators import only_integers, validate_file_size
from SU_Transportation.freights.validators import positive_number

user_model = get_user_model()


class LoadCreateModel(models.Model):
    MAX_LENGTH_LOAD_CITY = 100
    Load_Number = models.CharField(max_length=20, unique=True, validators=(only_integers,))
    Pickup = models.CharField(max_length=MAX_LENGTH_LOAD_CITY)
    Pickup_Address = models.TextField()
    Delivery = models.CharField(max_length=MAX_LENGTH_LOAD_CITY)
    Delivery_Address = models.TextField()
    Commodity = models.CharField(max_length=MAX_LENGTH_LOAD_CITY)
    Weight = models.FloatField(validators=(positive_number,))
    Pickup_Date = models.DateField()
    Pickup_Time = models.TimeField()
    Delivery_Date = models.DateField()
    Delivery_Time = models.TimeField()
    Load_POD = models.FileField(upload_to='documents', validators=(validate_file_size,), blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(user_model, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Load number: {self.Load_Number}'

@receiver(pre_delete, sender=LoadCreateModel)
def delete_related_file(sender, instance, **kwargs):
    if instance.Load_POD:
        file_path = instance.Load_POD.path
        if os.path.exists(file_path):
            os.remove(file_path)
