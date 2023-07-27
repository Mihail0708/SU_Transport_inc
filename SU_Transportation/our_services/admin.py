from django.contrib import admin

from SU_Transportation.our_services.models import ServicesModel


@admin.register(ServicesModel)
class DriverApplicationAdmin(admin.ModelAdmin):
    ordering = ['service_name']

