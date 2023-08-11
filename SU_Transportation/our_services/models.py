from django.db import models

from SU_Transportation.accounts.validators import validate_file_size


class ServicesModel(models.Model):
    service_picture = models.ImageField(upload_to='images', validators=(validate_file_size,))
    service_name = models.CharField(max_length=50)
    service_description = models.TextField()

    def __str__(self):
        return self.service_name



