import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MaxFileSizeValidator:
    message = _('Ensure this value is %(limit_value)s Mb. (it is %(show_value)s Mb.).')
    code = 'limit_value'

    def __init__(self, limit_value, message=None):
        self.limit_value = limit_value * 1024 * 1024  # Size in megabytes
        if message:
            self.message = message

    def __call__(self, value):
        cleaned = self.clean(value.size)
        params = {
            'limit_value': round(self.limit_value / 1024 / 1024, 2),
            'show_value': round(cleaned / 1024 / 1024, 2),
            'value': round(value.size / 1024 / 1024, 2)
        }
        if self.compare(cleaned, self.limit_value):
            raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__) and
                self.limit_value == other.limit_value and
                self.message == other.message and
                self.code == other.code
        )

    def compare(self, a, b):
        return a > b

    def clean(self, x):
        return x


def validate_rfc(value):
    regex = r"^([A-ZÑ\x26]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1]))([A-Z\d]{3})?$"
    if not re.match(regex, value):
        raise ValidationError(
            _('%(value)s is not a valid RFC.') % {'value': value},
            params={'value': value}
        )


def validate_hex_code(value):
    regex = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    if not re.match(regex, value):
        raise ValidationError(
            _('%(value)s is not a valid hexa code color.') % {'value': value},
            params={'value': value}
        )

# TODO Validador de tamaño de archivo con parametros
# TODO Validador de telefonos
