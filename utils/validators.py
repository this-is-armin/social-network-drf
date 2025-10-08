from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


INVALID_NAMES = [
    'username', 'email', 'first_name', 'last_name', 'password', 'confirm_password',
    'register', 'login', 'logout', 'signup', 'signin', 'signout', 'auth', 'users',
    'profile', 'edit', 'delete', 'update', 'remove',
]


def apply_regex(value, regex, message=None):
    RegexValidator(
        regex=regex,
        message=message or f"{value} is invalid.",
    )(value)


@deconstructible
class UsernameValidator:
    def __init__(self, invalid_names=None):
        self.invalid_names = invalid_names or INVALID_NAMES
    
    def __call__(self, value):
        apply_regex(
            value,
            r'^[a-z0-9_.]+$',
            'Username must contain only lowercase letters, numbers and _/.'
        )

        if value in INVALID_NAMES:
            raise ValidationError(f"{value} is not allowed as a username.")
        if value.isdigit():
            raise ValidationError('Username cannot be only numbers.')
        if all(char in '._' for char in value):
            raise ValidationError('Username cannot consist only of dots and underlines.')


@deconstructible
class NameValidator:
    def __init__(self, field_name='Name'):
        self.field_name = field_name
    
    def __call__(self, value):
        apply_regex(
            value,
            r'^[a-zA-z]+$',
            f"{self.field_name} must contain only letters."
        )