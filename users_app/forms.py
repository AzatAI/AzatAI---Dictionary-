from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .models import Users
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('First name')}),
                            label=("First name"), required=False)

    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('Last name')}),
                            label=("Last name"), required=False)

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': ('Email')}),
                            label=("Email"), required=True)

    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Phone')}),
                       label=("Phone number"), required=False)

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ('Password')}), label=("Password"))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ('Password')}), label=("Password"))

    class Meta:
        model = Users
        fields = ['first_name', 'last_name','phone_number', 'email', 'password1', 'password2']


class LogForm(forms.ModelForm):
    email_or_phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('email_or_phone')}),
                             label=("email_or_phone"), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ('Password')}), label=("Password"))
    class Meta:
        model = Users
        fields = ['email_or_phone', 'password']

    def clean(self):
        email_or_phone = self.cleaned_data['email_or_phone']
        password = self.cleaned_data['password']

        if not authenticate(email_or_phone=email_or_phone, password=password,):

            raise forms.ValidationError("Invalid login")

