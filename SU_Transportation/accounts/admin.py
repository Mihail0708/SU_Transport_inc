from django.contrib import admin
from django.contrib.auth import get_user_model

user_model = get_user_model()


@admin.register(user_model)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    search_fields = ['email', 'username']
    list_filter = ['username']


