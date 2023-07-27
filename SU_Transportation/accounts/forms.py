from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from SU_Transportation.accounts.models import SuUser

user_model = get_user_model()


class SuUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = user_model
        fields = ('username', 'email')


class SuUserEditForm(forms.ModelForm):
    class Meta:
        model = SuUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture', 'gender')
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'profile_picture': 'Image',
            'gender': 'Gender'
        }