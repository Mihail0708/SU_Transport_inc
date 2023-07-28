# Generated by Django 4.2.3 on 2023-07-14 15:31

import SU_Transportation.accounts.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ApplicationAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Street", models.CharField(max_length=100)),
                ("City", models.CharField(max_length=100)),
                (
                    "State",
                    models.CharField(
                        max_length=2,
                        validators=[django.core.validators.MinLengthValidator(2)],
                    ),
                ),
                (
                    "Zipcode",
                    models.CharField(
                        validators=[
                            django.core.validators.MaxLengthValidator(5),
                            django.core.validators.MinLengthValidator(5),
                            SU_Transportation.accounts.validators.only_integers,
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ContactUsModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=100)),
                ("Email", models.EmailField(max_length=254)),
                (
                    "Phone",
                    models.CharField(
                        validators=[
                            django.core.validators.MaxLengthValidator(10),
                            django.core.validators.MinLengthValidator(10),
                            SU_Transportation.accounts.validators.only_integers,
                        ]
                    ),
                ),
                ("Message", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="DriverApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "First_Name",
                    models.CharField(
                        validators=[
                            django.core.validators.MinLengthValidator(2),
                            django.core.validators.MaxLengthValidator(15),
                            SU_Transportation.accounts.validators.only_letters,
                        ]
                    ),
                ),
                (
                    "Last_Name",
                    models.CharField(
                        validators=[
                            django.core.validators.MinLengthValidator(2),
                            django.core.validators.MaxLengthValidator(15),
                            SU_Transportation.accounts.validators.only_letters,
                        ]
                    ),
                ),
                ("Data_of_Birth", models.DateField()),
                (
                    "Cell_Phone",
                    models.CharField(
                        validators=[
                            django.core.validators.MaxLengthValidator(10),
                            django.core.validators.MinLengthValidator(10),
                            SU_Transportation.accounts.validators.only_integers,
                        ]
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "SSL_Number",
                    models.CharField(
                        validators=[
                            django.core.validators.MaxLengthValidator(9),
                            django.core.validators.MinLengthValidator(9),
                            SU_Transportation.accounts.validators.only_integers,
                        ]
                    ),
                ),
                ("CDL_NUmber", models.CharField(max_length=15)),
                (
                    "address",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.applicationaddress",
                    ),
                ),
            ],
        ),
    ]