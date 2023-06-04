from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    """Оригинальный валидатор из django.contrib.auth.validators, но без @ и ."""
    regex = r"^[\w_+-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = 0
