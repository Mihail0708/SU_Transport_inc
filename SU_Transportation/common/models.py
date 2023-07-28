from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from SU_Transportation.accounts.validators import only_letters, only_integers


class ApplicationAddress(models.Model):
    Street = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=2, validators=(MinLengthValidator(2),))
    Zipcode = models.CharField(validators=(MaxLengthValidator(5), MinLengthValidator(5), only_integers))

    def __str__(self):
        return f'{self.Street} {self.City} {self.State} {self.Zipcode}'


class DriverApplication(models.Model):
    First_Name = models.CharField(validators=(MinLengthValidator(2), MaxLengthValidator(15), only_letters))
    Last_Name = models.CharField(validators=(MinLengthValidator(2), MaxLengthValidator(15), only_letters))
    Date_of_Birth = models.DateField()
    Date_applied = models.DateTimeField(auto_now_add=True)
    Cell_Phone = models.CharField(validators=(MaxLengthValidator(10), MinLengthValidator(10), only_integers))
    email = models.EmailField(unique=True)
    SSL_Number = models.CharField(validators=(MaxLengthValidator(9), MinLengthValidator(9), only_integers))
    CDL_NUmber = models.CharField(max_length=15)
    address = models.OneToOneField(ApplicationAddress, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.First_Name} {self.Last_Name}'


class ContactUsModel(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Phone = models.CharField(validators=(MaxLengthValidator(10), MinLengthValidator(10), only_integers))
    Message = models.TextField()
    is_red = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Name} {self.Email}'

