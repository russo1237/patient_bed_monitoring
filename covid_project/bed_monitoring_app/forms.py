from django import forms
from django.contrib.auth.models import User
from bed_monitoring_app.models import UserProfileInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    hospital_name = forms.CharField(required= True)
    address = forms.CharField(required= True)

    class Meta():
        model = UserProfileInfo
        fields = ('hospital_name', 'address')
