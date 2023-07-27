from django import forms

from SU_Transportation.freights.models import LoadCreateModel


class LoadCreateForm(forms.ModelForm):
    class Meta:
        model = LoadCreateModel
        fields = '__all__'
        exclude = ('Load_POD', 'is_completed', 'user')
        widgets = {
            'Pickup_Date': forms.DateInput(attrs={'type': 'date'}),
            'Delivery_Date': forms.DateInput(attrs={'type': 'date'}),
            'Pickup_Time': forms.TimeInput(attrs={'type': 'time'}),
            'Delivery_Time': forms.TimeInput(attrs={'type': 'time'})
        }


class CompleteLoadForm(forms.ModelForm):
    class Meta:
        model = LoadCreateModel
        fields = ('Load_Number', 'Load_POD')