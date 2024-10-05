from django.forms import Form
from django.forms import fields
from django.core.exceptions import ValidationError

from user.models import CustomUser


class SignupForm(Form):
    first_name = fields.CharField(
        required=False
    )
    last_name = fields.CharField(required=False)
    username = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            'required': 'Username cannot be empty',
            'min_length': 'Username must have at least 3 characters',
            'max_length': 'Username must have at most 18 characters',
        }
    )
    email = fields.EmailField(
        required=True,
        error_messages={
            'required': 'Email cannot be empty',
        },
    )
    password1 = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            'required': 'Password cannot be empty',
            'min_length': 'Password must have at least 3 characters',
            'max_length': 'Password must have at most 18 characters',
        }
    )
    password2 = fields.CharField(required=False)

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email

    def clean_password2(self):
        if not self.errors.get('password1'):
            if self.cleaned_data['password2'] != self.cleaned_data['password1']:
                raise ValidationError('Passwords do not match')
            return self.cleaned_data['password2']


class LoginForm(Form):
    username = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            'required': 'Username cannot be empty',
            'min_length': 'Username must have at least 3 characters',
            'max_length': 'Username must have at most 18 characters',
        }
    )
    password = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            'required': 'Password cannot be empty',
            'min_length': 'Password must have at least 3 characters',
            'max_length': 'Password must have at most 18 characters',
        }
    )


class EditProfileForm(Form):
    first_name = fields.CharField(
        required=False,
        min_length=1,
    )
    last_name = fields.CharField(
        required=False,
        min_length=1,
    )


class PasswordResetForm(Form):
    old_pwd = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            'required': 'Password cannot be empty',
            'min_length': 'Password must have at least 3 characters',
            'max_length': 'Password must have at most 18 characters',
        }
    )
    new_pwd = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            'required': 'Password cannot be empty',
            'min_length': 'Password must have at least 3 characters',
            'max_length': 'Password must have at most 18 characters',
        }
    )
    conf_pwd = fields.CharField(
        required=True,
        min_length=3,
        max_length=18,
        error_messages={
            'required': 'Password cannot be empty',
            'min_length': 'Password must have at least 3 characters',
            'max_length': 'Password must have at most 18 characters',
        }
    )

    def clean_new_pwd(self):
        if not self.errors.get('old_pwd'):
            if self.cleaned_data['new_pwd'] == self.cleaned_data['old_pwd']:
                raise ValidationError("New password cannot be same as the old password")
            return self.cleaned_data['new_pwd']

    def clean_conf_pwd(self):
        if not self.errors.get('new_pwd'):
            if self.cleaned_data['conf_pwd'] != self.cleaned_data['new_pwd']:
                raise ValidationError("Password confirmation doesn't match the password")
            return self.cleaned_data['conf_pwd']
