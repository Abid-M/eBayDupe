from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

# SignUp


class RegisterForm(UserCreationForm):
    dOB = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Account
        # All the different things the user signs up with.
        # They can add the other fields on the homepage!!
        fields = ['username', 'email', 'first_name', 'dOB']
        # 'phoneNumber', 'addressLine1', 'addressLine2', 'city', 'postcode', 'country']


class LogInUser(forms.Form):
    email = forms.EmailField(required=True)

    password = forms.CharField(widget=forms.PasswordInput)
