from django.contrib import admin

from SU_Transportation.common.models import DriverApplication


@admin.register(DriverApplication)
class DriverApplicationAdmin(admin.ModelAdmin):
    list_per_page = 10
    ordering = ['Date_applied']


