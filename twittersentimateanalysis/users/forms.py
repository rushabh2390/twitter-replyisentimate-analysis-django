from django import forms
from django.forms import fields
from .models import User

class UsersForm(forms.ModelForm):

    class Meta:
        model = User
        exclude =["userID"]
        widgets = {
            'userFirstName': forms.TextInput(),
            'userLastName': forms.TextInput(),
            'userEmail': forms.TextInput(),
            'userPwd': forms.TextInput(),
        },
        labels ={
            'userFirstName': 'First Name',
            'userLastName': 'Last Name',
            'userEmail':'Email',
            'userPwd':'Password',
        }

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields =["userEmail", "userPwd"]
        widgets = {
            'userEmail': forms.TextInput(),
            'userPwd': forms.PasswordInput()
        },
        labels ={
            'userEmail':'Email',
            'userPwd':'Password'
        }
