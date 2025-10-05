from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


INVALID_NAMES = [
    'username', 'email', 'first_name', 'last_name', 'password',
    'register', 'login', 'logout', 'auth', 'signup', 'signin', 'signout',
]

def username_validator(value):
    regex_validator = RegexValidator(
        regex=r'^[a-z0-9_.]+$',
        message='Username must contains only lowercase letters, numbers and _/.',
    )
    regex_validator(value)

    if value in INVALID_NAMES:
        raise ValidationError(f"{value} is not allowed as a username.")
    if value.isdigit():
        raise ValidationError('Username cannot be only numbers.')
    if all(char in '._' for char in value):
        raise ValidationError('Username cannot consist only of dots and underlines.')
    