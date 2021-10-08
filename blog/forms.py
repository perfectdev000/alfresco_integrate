from django import forms
from django.contrib.auth.password_validation import (get_default_password_validators,
                                     password_validators_help_text_html, 
                                     password_validators_help_texts)
from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext

class MinMaxLengthValidator:
    """
    Validate whether the password is of a minimum length.
    """
    def __init__(self, min_length=6, max_length=8):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "This password is too short. It must contain at least %(min_length)d character.",
                    "This password is too short. It must contain at least %(min_length)d characters.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )
        elif len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    f"This password is too big. It must contain maximum {self.max_length} character.",
                    f"This password is too big. It must contain maximum {self.max_length} characters.",
                    self.max_length
                ),
                code='password_too_short',
                params={'max_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at least %(min_length)d character.",
            "Your password must contain at least %(min_length)d characters.",
            self.min_length
        ) % {'min_length': self.min_length}
