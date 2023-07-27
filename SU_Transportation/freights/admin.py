from django.contrib import admin

from SU_Transportation.freights.models import LoadCreateModel


@admin.register(LoadCreateModel)
class LoadCreateAdmin(admin.ModelAdmin):
    list_per_page = 7
    ordering = ['Load_Number']

