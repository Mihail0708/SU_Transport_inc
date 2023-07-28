from django import forms

from SU_Transportation.common.models import DriverApplication, ApplicationAddress


class DriverApplicationForm(forms.ModelForm):
    class Meta:
        model = DriverApplication
        fields = '__all__'
        exclude = ['address', 'Date_applied']
        widgets = {
            'Date_of_Birth': forms.DateInput(attrs={'type': 'date'}),
        }


class ApplicationAddressForm(forms.ModelForm):
    class Meta:
        model = ApplicationAddress
        fields = '__all__'

