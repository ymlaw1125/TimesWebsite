from django.forms import Form
from django.forms import fields
from django.core.exceptions import ValidationError

from user.models import CustomUser


class SignupForm(Form):
    username = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            "required": "Username cannot be empty",
            "min_length": "Username must have at least 3 characters",
            "max_length": "Username must have at most 18 characters",
        }
    )
    password1 = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            "required": "Password cannot be empty",
            "min_length": "Password must have at least 3 characters",
            "max_length": "Password must have at most 18 characters",
        }
    )
    password2 = fields.CharField(required=False)
    email = fields.EmailField(
        required=True,
        error_messages={
            "required": "Email cannot be empty",
        },
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        if not self.errors.get("password1"):
            if self.cleaned_data["password2"] != self.cleaned_data["password1"]:
                raise ValidationError("Passwords do not match")
            return self.cleaned_data


class LoginForm(Form):
    username = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            "required": "Username cannot be empty",
            "min_length": "Username must have at least 3 characters",
            "max_length": "Username must have at most 18 characters",
        }
    )
    password = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            "required": "Password cannot be empty",
            "min_length": "Password must have at least 3 characters",
            "max_length": "Password must have at most 18 characters",
        }
    )
