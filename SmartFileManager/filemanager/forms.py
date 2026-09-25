from django import forms

from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm
)

from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):

    username = forms.CharField(

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "Username",

                "autocomplete": "username",

            }

        )

    )


    password = forms.CharField(

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control",

                "placeholder": "Password",

                "autocomplete": "current-password",

            }

        )

    )


class RegisterForm(UserCreationForm):

    username = forms.CharField(

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "Choose a username",

            }

        )

    )


    password1 = forms.CharField(

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control",

                "placeholder": "Create password",

            }

        )

    )


    password2 = forms.CharField(

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control",

                "placeholder": "Confirm password",

            }

        )

    )


    class Meta:

        model = User

        fields = (

            "username",

            "password1",

            "password2",

        )