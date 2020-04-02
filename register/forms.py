from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    # When we use this 'RegisterForm' we want to save it into the User database. To do that
    # we need to include 'Meta' class. Here I say model is equal to the user db. Now I'm going to include those
    # fields that I want to show on the Registration page.
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
